import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
    const logout = async (e) => {
        e.preventDefault();
        let logout_url = window.location.origin + "/logout";
        const res = await fetch(logout_url, {
            method: "POST",
        });

        const json = await res.json();
        if (res.ok) {
            let username = sessionStorage.getItem('username');
            sessionStorage.removeItem('username');
            window.location.href = window.location.origin;
            window.location.reload();
            alert("Logging out " + username + "...");
        } else {
            alert(json.message || "The user could not be logged out.");
        }
    };

    //The default home page items are the login details panel
    let home_page_items = <div></div>;

    //Gets the username in the current session
    let curr_user = sessionStorage.getItem('username');

    //If the user is logged in, show the username and logout option on home page
    if (curr_user !== null && curr_user !== "") {
        home_page_items = (
            <div className="input_panel">
                <text className='username'>{sessionStorage.getItem("username")}</text>
                <button className="nav_item" onClick={logout}>
                    Logout
                </button>
            </div>
        );
    }

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: "darkturquoise", height: "1in" }}>
                <div className="container-fluid">
                    <h2 style={{ paddingRight: "5%" }}>Dealerships</h2>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarText">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <a className="nav-link active" style={{ fontSize: "larger" }} aria-current="page" href="/">Home</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" style={{ fontSize: "larger" }} href="/about">About Us</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" style={{ fontSize: "larger" }} href="/contact">Contact Us</a>
                            </li>
                        </ul>
                        <span className="navbar-text">
                            <div className="loginlink" id="loginlogout">
                                {home_page_items}
                            </div>
                        </span>
                    </div>
                </div>
            </nav>
        </div>
    )
}

export default Header
