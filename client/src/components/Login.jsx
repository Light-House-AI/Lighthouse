import React, { useState } from "react";
import axios from "axios";

function Login() {
    const [year] = useState(new Date().getFullYear());

    const togglePassword = function (e) {
        if (e.currentTarget.attributes["data-password"].value === "false") {
            e.currentTarget.previousElementSibling.attributes['type'].value = "text";
            e.currentTarget.attributes["data-password"].value = "true";
            e.currentTarget.classList.add("show-password");
        } else {
            e.currentTarget.previousElementSibling.attributes['type'].value = "password";
            e.currentTarget.attributes["data-password"].value = "false";
            e.currentTarget.classList.remove("show-password");
        }
    }

    return (
        <div className="account-pages d-flex justify-content-center align-items-center vh-100">
            <div className="container">
                <div className="row justify-content-center align-items-center">
                    <div className="col-md-8 col-lg-6 col-xl-4">
                        <div className="card bg-pattern">
                            <div className="card-body p-4">
                                <div className="text-center w-75 m-auto">
                                    <div className="auth-logo">
                                        <a href="index.html" className="logo logo-dark text-center">
                                            <span className="logo-lg">
                                                <img src="/logo-dark.png" alt="" height="22" />
                                            </span>
                                        </a>

                                        <a href="index.html" className="logo logo-light text-center">
                                            <span className="logo-lg">
                                                <img src="/logo-light.png" alt="" height="22" />
                                            </span>
                                        </a>
                                    </div>
                                </div>
                                <div className="my-3">
                                    <label htmlFor="emailaddress" className="form-label">Email address</label>
                                    <input className="form-control" type="email" id="emailaddress" required="" placeholder="Enter your email" />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">Password</label>
                                    <div className="input-group input-group-merge">
                                        <input type="password" className="form-control" placeholder="Enter your password" />
                                        <div className="input-group-text cursor-pointer" data-password="false" onClick={(e) => { togglePassword(e); }}>
                                            <span className="password-eye"></span>
                                        </div>
                                    </div>
                                </div>
                                <div className="text-center d-grid">
                                    <button className="btn btn-primary" type="submit"> Log In </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-12">
                        <footer className="footer footer-alt text-white-50">
                            {year} &copy; <a href="/">Lighthouse AI</a>
                        </footer>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;