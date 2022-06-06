import React, { useEffect, useState } from "react";
import { Redirect, Route, Switch } from "react-router-dom";
import { Routes } from "../routes";

// L&D Platform
import PlatformDashboard from "./dashboard/Dashboard";
import NewsTracker from "./bots/NewsTracker";
import MyBots from "./my/Bots";
import MySettings from "./my/Settings";
import Login from "./auth/LogIn";
import Signup from "./auth/Signup";
import ForgotPassword from "./auth/ForgotPassword";
import ResetPassword from "./auth/ResetPassword";
import NotFoundPage from "./errors/NotFound";
import ServerError from "./errors/ServerError";

// components
import Sidebar from "../components/Sidebar";
import UserInfoNavBar from "../components/Navbar";
import Preloader from "../components/Preloader";
import useUserStore from "../store/user_store_context";

const RouteWithLoader = ({ component: Component, ...rest }) => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Route
      {...rest}
      render={props => (
        <>
          {" "}
          <Preloader show={!loaded} /> <Component {...props} />{" "}
        </>
      )}
    />
  );
};

const RouteWithSidebar = ({ component: Component, ...rest }) => {
  const [loaded, setLoaded] = useState(false);
  const userStore = useUserStore();

  useEffect(() => {
    const timer = setTimeout(() => setLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  if (userStore.isUserInfoEmpty) {
    userStore.updateUserInfo();
  }

  return (
    <Route
      {...rest}
      render={props => (
        <>
          <Preloader show={!loaded} />
          <Sidebar />

          <main className="content">
            <UserInfoNavBar />
            <Component {...props} />
          </main>
        </>
      )}
    />
  );
};

export default () => (
  <Switch>
    {/* L&D Platform Pages */}
    <RouteWithSidebar
      exact
      path={Routes.PlatformDashboard.path}
      component={PlatformDashboard}
    />
    <RouteWithSidebar
      exact
      path={Routes.NewsTrackerBot.path}
      component={NewsTracker}
    />
    <RouteWithSidebar exact path={Routes.MyBots.path} component={MyBots} />
    <RouteWithSidebar
      exact
      path={Routes.MyTrades.path}
      component={NotFoundPage}
    />
    <RouteWithSidebar
      exact
      path={Routes.MySettings.path}
      component={MySettings}
    />
    <RouteWithLoader exact path={Routes.Login.path} component={Login} />
    <RouteWithLoader exact path={Routes.Signup.path} component={Signup} />
    <RouteWithLoader
      exact
      path={Routes.ForgotPassword.path}
      component={ForgotPassword}
    />
    <RouteWithLoader
      exact
      path={Routes.ResetPassword.path}
      component={ResetPassword}
    />
    <RouteWithLoader
      exact
      path={Routes.NotFound.path}
      component={NotFoundPage}
    />
    <RouteWithLoader
      exact
      path={Routes.ServerError.path}
      component={ServerError}
    />

    {/* Global */}
    <Redirect to={Routes.NotFound.path} />
  </Switch>
);
