import React from "react";

import Login from "../components/Login";

function LoginPage() {
    return (
        <div id='loginpage' className="scroll">
            <title>Login | Lighthouse AI</title>
            <div className="container-fluid">
                <Login />
            </div>
        </div>
    );
}

export default LoginPage;