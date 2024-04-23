import React from "react";

const UserContext = React.createContext({ username: '', email: '', auth: false });

const UserProvider = ({ children }) => {
    // User is the name of the "data" that gets stored in context
    const [user, setUser] = React.useState({ username: '', email: '', auth: true });

    // Login updates the user data with a name parameter
    const loginContext = (username) => {
        setUser((user) => ({
            username: username,
            auth: true,
        }));
    };

    // Logout updates the user data to default
    const logout = () => {
        localStorage.removeItem("access_token")
        sessionStorage.clear();
        localStorage.clear();
        setUser((user) => ({
            username: '',
            email: '',
            auth: false,
        }));
    };

    return (
        <UserContext.Provider value={{ user, loginContext, logout }}>
            {children}
        </UserContext.Provider>
    );
}

export { UserContext, UserProvider }