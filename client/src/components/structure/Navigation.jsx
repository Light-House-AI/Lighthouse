import React, { useState } from "react";

function Navigation() {

    const [location] = useState(window.location.pathname);

    function openFullscreen() {
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.webkitRequestFullscreen) { /* Safari */
            document.documentElement.webkitRequestFullscreen();
        } else if (document.documentElement.msRequestFullscreen) { /* IE11 */
            document.documentElement.msRequestFullscreen();
        }
    }

    function minimizeSidebar() {
        if (document.body.attributes['data-sidebar-size'].value === 'condensed')
            document.body.attributes['data-sidebar-size'].value = 'default';
        else
            document.body.attributes['data-sidebar-size'].value = 'condensed';
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
                            <span className="badge bg-danger rounded-circle noti-icon-badge">9</span>
                        </button>
                        <div className="dropdown-menu dropdown-menu-end dropdown-lg">
                            <div className="dropdown-item noti-title">
                                <h5 className="m-0">
                                    <span className="float-end">
                                        <button className="text-dark button-no-style">
                                            <small>Clear All</small>
                                        </button>
                                    </span>Notification
                                </h5>
                            </div>

                            <div className="noti-scroll" data-simplebar>
                                <a href="/" className="dropdown-item notify-item active">
                                    <div className="notify-icon">
                                        <img src="../assets/images/users/user-1.jpg" className="img-fluid rounded-circle" alt="" /> </div>
                                    <p className="notify-details">Cristina Pride</p>
                                    <p className="text-muted mb-0 user-msg">
                                        <small>Hi, How are you? What about our next meeting</small>
                                    </p>
                                </a>

                                <a href="/" className="dropdown-item notify-item">
                                    <div className="notify-icon bg-primary">
                                        <i className="mdi mdi-comment-account-outline"></i>
                                    </div>
                                    <p className="notify-details">Caleb Flakelar commented on Admin
                                        <small className="text-muted">1 min ago</small>
                                    </p>
                                </a>

                                <a href="/" className="dropdown-item notify-item">
                                    <div className="notify-icon">
                                        <img src="../assets/images/users/user-4.jpg" className="img-fluid rounded-circle" alt="" /> </div>
                                    <p className="notify-details">Karen Robinson</p>
                                    <p className="text-muted mb-0 user-msg">
                                        <small>Wow ! this admin looks good and awesome design</small>
                                    </p>
                                </a>

                                <a href="/" className="dropdown-item notify-item">
                                    <div className="notify-icon bg-warning">
                                        <i className="mdi mdi-account-plus"></i>
                                    </div>
                                    <p className="notify-details">New user registered.
                                        <small className="text-muted">5 hours ago</small>
                                    </p>
                                </a>

                                <a href="/" className="dropdown-item notify-item">
                                    <div className="notify-icon bg-info">
                                        <i className="mdi mdi-comment-account-outline"></i>
                                    </div>
                                    <p className="notify-details">Caleb Flakelar commented on Admin
                                        <small className="text-muted">4 days ago</small>
                                    </p>
                                </a>

                                <a href="/" className="dropdown-item notify-item">
                                    <div className="notify-icon bg-secondary">
                                        <i className="mdi mdi-heart"></i>
                                    </div>
                                    <p className="notify-details">Carlos Crouch liked
                                        <b>Admin</b>
                                        <small className="text-muted">13 days ago</small>
                                    </p>
                                </a>
                            </div>

                            <a href="/" className="dropdown-item text-center text-primary notify-item notify-all">
                                View all
                                <i className="fe-arrow-right"></i>
                            </a>

                        </div>
                    </li>

                    {/* User */}
                    <li className="dropdown notification-list topbar-dropdown">
                        <button className="nav-link dropdown-toggle nav-user me-0 waves-effect waves-light arrow-none button-no-style" data-bs-toggle="dropdown" aria-haspopup="false" aria-expanded="false">
                            <img src="user.jpg" className="rounded-circle" alt='' />
                            <span className="pro-user-name ms-1">
                                Stanley <i className="mdi mdi-chevron-down"></i>
                            </span>
                        </button>
                        <div className="dropdown-menu dropdown-menu-end profile-dropdown ">
                            <div className="dropdown-header noti-title">
                                <h6 className="text-overflow m-0">Welcome !</h6>
                            </div>
                            <div className="dropdown-divider"></div>
                            <a href="/login" className="dropdown-item notify-item">
                                <i className="fe-log-out"></i>
                                <span>Logout</span>
                            </a>
                        </div>
                    </li>

                </ul>

                {/* LOGO */}
                <div className="logo-box">
                    <a href="/" className="logo logo-light text-center">
                        <span className="logo-sm">
                            <img src="logo-sm.png" alt="" height="22" />
                        </span>
                        <span className="logo-lg">
                            <img src="logo-light.png" alt="" height="20" />
                        </span>
                    </a>
                </div>

                {/* SIDE MENU */}
                <ul className="list-unstyled topnav-menu topnav-menu-left m-0">
                    {location !== '/' ?
                        <li>
                            <button className="button-menu-mobile waves-effect waves-light" onClick={minimizeSidebar}>
                                <i className="fe-menu"></i>
                            </button>
                        </li> : null
                    }
                    <li className="dropdown d-none d-md-block">
                        <a className="nav-link waves-effect waves-light" href="/" role="button">
                            Create New Project
                        </a>
                    </li>
                    <li className="dropdown d-block d-md-none">
                        <a className="nav-link waves-effect waves-light" href="/" role="button">
                            <i className="fe-plus"></i>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default Navigation;