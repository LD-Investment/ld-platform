import PlaceholderImage from "../assets/img/placeholder.png";

import { Routes } from "../routes";

export default [
  {
    id: 1,
    name: "AI/Quant Fund",
    image: PlaceholderImage,
    link: Routes.AutoBotView.path
  },
  {
    id: 2,
    name: "Indicator Bot",
    image: PlaceholderImage,
    link: Routes.IndicatorBotView.path
  },
  {
    id: 3,
    name: "Manual Bot",
    image: PlaceholderImage,
    link: Routes.ManualBotView.path
  },
  {
    id: 4,
    name: "Insightful reports",
    image: PlaceholderImage,
    link: Routes.ReportView.path
  }
];
