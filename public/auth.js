// Supabase configuration
const SUPABASE_URL = 'https://hqznqbpexocovhyagwmm.supabase.co';
const SUPABASE_KEY = 'sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d';

// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// Check if user is authenticated
async function checkAuth() {
    const { data: { session } } = await supabase.auth.getSession();
    return session;
}

// Email/Password Sign Up
async function signUp(email, password) {
    try {
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password
        });
        
        if (error) throw error;
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Email/Password Sign In
async function signIn(email, password) {
    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });
        
        if (error) throw error;
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Google OAuth Sign In
async function signInWithGoogle() {
    try {
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: {
                redirectTo: window.location.origin + '/characters'
            }
        });
        
        if (error) throw error;
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Sign Out
async function signOut() {
    try {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Get current user
async function getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
}

// Get current session
async function getSession() {
    const { data: { session } } = await supabase.auth.getSession();
    return session;
}

// Listen for auth state changes
supabase.auth.onAuthStateChange((event, session) => {
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

// Export functions
window.supabaseAuth = {
    supabase,
    checkAuth,
    signUp,
    signIn,
    signInWithGoogle,
    signOut,
    getCurrentUser,
    getSession
};
