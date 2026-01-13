// Prevent duplicate initialization
(function() {
    if (window.supabaseAuth) {
        console.warn('Supabase auth already initialized');
        return;
    }
    
    // Supabase configuration
    const SUPABASE_URL = 'https://hqznqbpexocovhyagwmm.supabase.co';
    const SUPABASE_KEY = 'sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d';

    // Wait for Supabase library to load and initialize
    function waitForSupabase() {
        return new Promise((resolve, reject) => {
            let attempts = 0;
            const maxAttempts = 50; // 5 seconds max
            
            const checkSupabase = () => {
                attempts++;
                
                // Check if Supabase is available (CDN exposes it as window.supabase)
                if (typeof window.supabase !== 'undefined' && window.supabase.createClient) {
                    resolve(window.supabase.createClient);
                    return;
                }
                
                if (attempts >= maxAttempts) {
                    reject(new Error('Supabase library failed to load'));
                    return;
                }
                
                setTimeout(checkSupabase, 100);
            };
            
            checkSupabase();
        });
    }
    
    // Initialize Supabase client
    let supabaseClient = null;
    
    waitForSupabase()
        .then((createClient) => {
            supabaseClient = createClient(SUPABASE_URL, SUPABASE_KEY);
            console.log('Supabase client initialized');
            
            // Export functions once client is ready
            window.supabaseAuth = {
                supabase: supabaseClient,
                checkAuth,
                signUp,
                signIn,
                signInWithGoogle,
                signOut,
                getCurrentUser,
                getSession
            };
        })
        .catch((error) => {
            console.error('Failed to initialize Supabase:', error);
            // Export error handler
            window.supabaseAuth = {
                error: error.message,
                checkAuth: () => Promise.reject(error),
                signUp: () => Promise.resolve({ success: false, error: 'Supabase not loaded' }),
                signIn: () => Promise.resolve({ success: false, error: 'Supabase not loaded' }),
                signInWithGoogle: () => Promise.resolve({ success: false, error: 'Supabase not loaded' }),
                signOut: () => Promise.resolve({ success: false, error: 'Supabase not loaded' }),
                getCurrentUser: () => Promise.resolve(null),
                getSession: () => Promise.resolve(null)
            };
        });

    // Check if user is authenticated
    async function checkAuth() {
        if (!supabaseClient) {
            throw new Error('Supabase client not initialized');
        }
        const { data: { session } } = await supabaseClient.auth.getSession();
        return session;
    }

    // Email/Password Sign Up
    async function signUp(email, password) {
        if (!supabaseClient) {
            return { success: false, error: 'Supabase client not initialized' };
        }
        try {
            const { data, error } = await supabaseClient.auth.signUp({
                email: email,
                password: password,
                options: {
                    emailRedirectTo: window.location.origin + '/characters'
                }
            });
            
            if (error) throw error;
            
            // Check if email confirmation is required
            if (data.user && !data.session) {
                // Email confirmation required
                return { 
                    success: true, 
                    data, 
                    requiresConfirmation: true,
                    message: 'Please check your email to confirm your account before signing in.'
                };
            }
            
            return { success: true, data };
        } catch (error) {
            console.error('Sign up error:', error);
            return { success: false, error: error.message || 'Failed to create account' };
        }
    }

    // Email/Password Sign In
    async function signIn(email, password) {
        if (!supabaseClient) {
            return { success: false, error: 'Supabase client not initialized' };
        }
        try {
            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email: email,
                password: password
            });
            
            if (error) {
                // Handle specific error cases
                if (error.message.includes('Email not confirmed')) {
                    throw new Error('Please check your email and click the confirmation link before signing in.');
                }
                throw error;
            }
            
            if (!data.session) {
                return { 
                    success: false, 
                    error: 'No session created. Please check your email for confirmation.' 
                };
            }
            
            return { success: true, data };
        } catch (error) {
            console.error('Sign in error:', error);
            return { success: false, error: error.message || 'Failed to sign in' };
        }
    }

    // Google OAuth Sign In
    async function signInWithGoogle() {
        if (!supabaseClient) {
            return { success: false, error: 'Supabase client not initialized' };
        }
        try {
            const redirectUrl = window.location.origin + '/characters';
            console.log('Initiating Google OAuth, redirect to:', redirectUrl);
            
            const { data, error } = await supabaseClient.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: redirectUrl
                }
            });
            
            if (error) {
                console.error('OAuth error:', error);
                throw error;
            }
            
            // If we get a URL back, we need to redirect to it (OAuth flow)
            if (data?.url) {
                console.log('Redirecting to OAuth provider:', data.url);
                window.location.href = data.url;
                return { success: true, data, redirecting: true };
            }
            
            return { success: true, data };
        } catch (error) {
            console.error('Google OAuth error:', error);
            return { success: false, error: error.message || 'Failed to sign in with Google' };
        }
    }

    // Sign Out
    async function signOut() {
        if (!supabaseClient) {
            return { success: false, error: 'Supabase client not initialized' };
        }
        try {
            const { error } = await supabaseClient.auth.signOut();
            if (error) throw error;
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Get current user
    async function getCurrentUser() {
        if (!supabaseClient) {
            return null;
        }
        const { data: { user } } = await supabaseClient.auth.getUser();
        return user;
    }

    // Get current session
    async function getSession() {
        if (!supabaseClient) {
            return null;
        }
        const { data: { session } } = await supabaseClient.auth.getSession();
        return session;
    }

    // Listen for auth state changes (once client is ready)
    waitForSupabase().then((createClient) => {
        if (!supabaseClient) {
            supabaseClient = createClient(SUPABASE_URL, SUPABASE_KEY);
        }
        
        supabaseClient.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_OUT' || !session) {
                // Redirect to login if not on login page
                if (window.location.pathname !== '/' && !window.location.pathname.includes('index.html')) {
                    window.location.href = '/';
                }
            } else if (event === 'SIGNED_IN' && session) {
                // Redirect to characters page if on login page
                if (window.location.pathname === '/' || window.location.pathname.includes('index.html')) {
                    window.location.href = '/characters';
                }
            }
        });
    });
})();
