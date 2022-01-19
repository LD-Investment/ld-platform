import AiQuantBotImage from "../assets/img/pages/landing_page/3-funds-ai_quant_bot.png";
import IndicatorBotImage from "../assets/img/pages/landing_page/3-funds-indicator_bot.png";
import ManualBotImage from "../assets/img/pages/landing_page/3-funds-manual_bot.png";
import ReportServiceImage from "../assets/img/pages/landing_page/3-funds-report_service.png";

import { Routes } from "../routes";

export default [
  {
    id: 1,
    name: "AI/Quant Fund",
    image: AiQuantBotImage,
    link: Routes.AutoBotView.path
  },
  {
    id: 2,
    name: "Indicator Bot",
    image: IndicatorBotImage,
    link: Routes.IndicatorBotView.path
  },
  {
    id: 3,
    name: "Manual Bot",
    image: ManualBotImage,
    link: Routes.ManualBotView.path
  },
  {
    id: 4,
    name: "Insightful reports",
    image: ReportServiceImage,
    link: Routes.ReportView.path
  }
];
