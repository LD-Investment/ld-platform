import OverviewImg from "../assets/img/pages/overview.jpg";
import TransactionsImg from "../assets/img/pages/transactions.jpg";
import SettingsImg from "../assets/img/pages/settings.jpg";
import PlaceholderImage from "../assets/img/placeholder.png";
import SignInImg from "../assets/img/pages/sign-in.jpg";

import { Routes } from "../routes";

export default [
  {
    id: 1,
    name: "AI/Quant Fund",
    image: PlaceholderImage,
    link: Routes.DashboardOverview.path
  },
  {
    id: 2,
    name: "Indicator Bot",
    image: PlaceholderImage,
    link: Routes.Transactions.path
  },
  {
    id: 3,
    name: "Manual Bot",
    image: PlaceholderImage,
    link: Routes.Settings.path
  },
  {
    id: 4,
    name: "Insightful reports",
    image: PlaceholderImage,
    link: Routes.Accordions.path
  }
];
