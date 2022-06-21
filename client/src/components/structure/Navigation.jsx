import React, { useState, useEffect } from "react";
import axios from "axios";

function Navigation() {
    const [userDetails] = useState(JSON.parse(localStorage.getItem("user")));
    const [notifications, setNotifications] = useState(null);
    const [location] = useState(window.location.pathname);

    useEffect(() => {
        axios.defaults.baseURL = "http://localhost:8000/api/v1";
        window.baseURL = "http://localhost:8000/api/v1";

        axios.interceptors.response.use(
            response => response,
            error => {
                if (error.response.status === 401) {
                    localStorage.clear();
                    window.location.href = "/login";
                }
                return Promise.reject(error);
            }
        );

        window.getNotifications = function() {
            axios.get('/users/notifications', {
                headers: {
                    'Authorization': `${localStorage.getItem('tokenType')} ${localStorage.getItem('accessToken')}`
                }
            }).then((response) => {
                setNotifications(response.data);
            });
        }
        window.getNotifications();
        window.notificationsIntervalId = window.setInterval(window.getNotifications, 5000);


    }, []);

    function openFullscreen() {
        window.$('body').toggleClass('fullscreen-enable');
        if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement) {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            } else if (document.documentElement.mozRequestFullScreen) {
                document.documentElement.mozRequestFullScreen();
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
            }
        } else {
            if (document.cancelFullScreen) {
                document.cancelFullScreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitCancelFullScreen) {
                document.webkitCancelFullScreen();
            }
        }
    }

    function minimizeSidebar() {
        if (document.body.attributes['data-sidebar-size'].value === 'condensed')
            document.body.attributes['data-sidebar-size'].value = 'default';
        else
            document.body.attributes['data-sidebar-size'].value = 'condensed';
    }

    function logOut() {
        localStorage.clear();
        window.location.href = "/login";
    }

    return (
        <div className="navbar-custom">
            <div className="container-fluid">
                <ul className="list-unstyled topnav-menu float-end mb-0">

                    {/* Fullscreen */}
                    <li className="dropdown d-none d-lg-inline-block">
                        <button className="nav-link dropdown-toggle arrow-none waves-effect waves-light button-no-style" data-toggle="fullscreen" onClick={openFullscreen}>
                            <i className="fe-maximize fullscreen-icon"></i>
                        </button>
                    </li>

                    {/* Notifications */}
                    <li className="dropdown notification-list topbar-dropdown">
                        <button className="nav-link dropdown-toggle waves-effect waves-light button-no-style" data-bs-toggle="dropdown" aria-haspopup="false" aria-expanded="false">
                            <i className="fe-bell noti-icon"></i>
                            {notifications !== null && notifications.length > 0 ?
                                <span className="badge bg-danger rounded-circle noti-icon-badge">
                                    {notifications !== null ? notifications.length : 0}
                                </span> : null}
                        </button>
                        <div className="dropdown-menu dropdown-menu-end dropdown-lg">
                            <div className="dropdown-item noti-title">
                                <h5 className="m-0">
                                    <span className="float-end">
                                        {/* <button className="text-dark button-no-style">
                                            <small>Clear All</small>
                                        </button> */}
                                    </span>Notification
                                </h5>
                            </div>

                            <div className="noti-scroll" data-simplebar>
                                {notifications !== null ?
                                    notifications.map((notification, index) => {
                                        return (
                                            <a href="/" className="dropdown-item notify-item" key={index}>
                                                <div className="notify-icon bg-primary">
                                                    <i className="mdi mdi-comment-account-outline"></i>
                                                </div>
                                                <p className="notify-details">{notification.title}</p>
                                                <p className="text-muted mb-0 user-msg">
                                                    <small>{notification.body}.</small>
                                                </p>
                                            </a>
                                        );
                                    })
                                    :
                                    <div className="dropdown-item notify-item text-center">
                                        <small>No notification found.</small>
                                    </div>}
                            </div>

                            {/* <a href="/" className="dropdown-item text-center text-primary notify-item notify-all">
                                View all
                                <i className="fe-arrow-right"></i>
                            </a> */}

                        </div>
                    </li>

                    {/* User */}
                    <li className="dropdown notification-list topbar-dropdown">
                        <button className="nav-link dropdown-toggle nav-user me-0 waves-effect waves-light arrow-none button-no-style" data-bs-toggle="dropdown" aria-haspopup="false" aria-expanded="false">
                            <img src="/user.jpg" className="rounded-circle" alt='' />
                            <span className="pro-user-name ms-1">
                                {userDetails.first_name} <i className="mdi mdi-chevron-down"></i>
                            </span>
                        </button>
                        <div className="dropdown-menu dropdown-menu-end profile-dropdown ">
                            <div className="dropdown-header noti-title">
                                <h6 className="text-overflow m-0">Welcome !</h6>
                            </div>
                            <div className="dropdown-divider"></div>
                            <button className="dropdown-item notify-item" onClick={logOut}>
                                <i className="fe-log-out"></i>
                                <span>Logout</span>
                            </button>
                        </div>
                    </li>

                </ul>

                {/* LOGO */}
                <div className="logo-box">
                    <a href="/" className="logo logo-light text-center">
                        <span className="logo-sm">
                            <img src="/logo-sm.png" alt="" height="22" />
                        </span>
                        <span className="logo-lg">
                            <img src="/logo-light.png" alt="" height="20" />
                        </span>
                    </a>
                </div>

                {/* SIDE MENU */}
                <ul className="list-unstyled topnav-menu topnav-menu-left m-0">
                    {location !== '/' && location !== '/newproject' ?
                        <li>
                            <button className="button-menu-mobile waves-effect waves-light" onClick={minimizeSidebar}>
                                <i className="fe-menu"></i>
                            </button>
                        </li> : null
                    }
                    <li className="dropdown d-none d-md-block">
                        <a className="nav-link waves-effect waves-light" href="/newproject">
                            Create New Project
                        </a>
                    </li>
                    <li className="dropdown d-block d-md-none">
                        <a className="nav-link waves-effect waves-light" href="/newproject">
                            <i className="fe-plus"></i>
                        </a>
                    </li>
                </ul>
            </div>
        </div >
    );
}

export default Navigation;