import OverviewImg from "../assets/img/pages/overview.jpg";
import TransactionsImg from "../assets/img/pages/transactions.jpg";
import SettingsImg from "../assets/img/pages/settings.jpg";
import SignInImg from "../assets/img/pages/sign-in.jpg";

import { Routes } from "../routes";

export default [
  {
    id: 1,
    name: "AI/Quant Fund",
    image: OverviewImg,
    link: Routes.DashboardOverview.path
  },
  {
    id: 2,
    name: "Indicator Bot",
    image: TransactionsImg,
    link: Routes.Transactions.path
  },
  {
    id: 3,
    name: "Manual Bot",
    image: SettingsImg,
    link: Routes.Settings.path
  },
  {
    id: 4,
    name: "Insightful reports",
    image: SignInImg,
    link: Routes.Accordions.path
  }
];
