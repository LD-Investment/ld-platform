export const Routes = {
  // L&D Platform
  PlatformDashboard: { path: "/" },

  NewsTrackerBot: { path: "/bots/news-tracker" },

  MyBots: { path: "/user/bots" },
  MyTrades: { path: "/user/trades" },
  MySettings: { path: "/user/settings" },

  Login: { path: "/auth/login" },
  Signup: { path: "/auth/signup" },
  ForgotPassword: { path: "/auth/forgot-password" },
  ResetPassword: { path: "/auth/reset-password" },

  NotFound: { path: "/errors/404" },
  ServerError: { path: "/errors/500" }
};
