import { createContext } from "react";
import { useLocalStorage } from "@uidotdev/usehooks";

export const AuthContext = createContext({});

export function AuthProvider ({ children }) {
    const [auth, setAuth] = useLocalStorage("auth", null);

    return (
        <AuthContext.Provider value={{ auth, setAuth }}>
            {children}
        </AuthContext.Provider>
    )
}
