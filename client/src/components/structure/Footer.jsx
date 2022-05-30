import React, { useState } from 'react';

function Footer() {
    const [year] = useState(new Date().getFullYear());
    return (
        <div className="footer">
            <div className="row">
                <div className="col-md-6">
                    {year} &copy; <a href="/">Lighthouse AI</a>
                </div>
                <div className="col-md-6">
                    <div className="text-md-end footer-links d-none d-sm-block">
                        <a href="/">About Us</a>
                        <a href="/">Help</a>
                        <a href="/">Contact Us</a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Footer;