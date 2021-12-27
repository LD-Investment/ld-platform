export const Routes = {
  // L&D Landing page
  LandingView: { path: "/" },
  AutoBotView: { path: "/product/auto-bot " },
  ManualBotView: { path: "/product/manual-bot " },
  IndicatorBotView: { path: "/product/indicator-bot " },
  ReportView: { path: "/product/report" },

  // L&D Platform
  PlatformDashboard: { path: "/platform/dashboard" },

  MyBots: { path: "/platform/user/bots" },
  MyTrades: { path: "/platform/user/trades" },
  MySettings: { path: "/platform/user/settings" },

  Signin: { path: "/platform/auth/sign-in" },
  Signup: { path: "/platform/auth/sign-up" },
  ForgotPassword: { path: "/platform/auth/forgot-password" },
  ResetPassword: { path: "/platform/auth/reset-password" },

  NotFound: { path: "/errors/404" },
  ServerError: { path: "/errors/500" }
};
