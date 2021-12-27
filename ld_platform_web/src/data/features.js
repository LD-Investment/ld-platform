import { faMobileAlt } from "@fortawesome/free-solid-svg-icons";
import {
  faBootstrap,
  faReact,
  faSass
} from "@fortawesome/free-brands-svg-icons";
import { Routes } from "../routes";

export default [
  {
    id: 0,
    title: "AI/Quant Fund",
    icon: faReact,
    description: "Blabla blabla blabla Blabla blabla blabla",
    link: Routes.NotFound.path
  },
  {
    id: 1,
    title: "Indicator Bot",
    icon: faBootstrap,
    description: "Blabla blabla blabla Blabla blabla blabla",
    link: Routes.NotFound.path
  },
  {
    id: 2,
    title: "Manual Bot",
    icon: faSass,
    description: "Blabla blabla blabla Blabla blabla blabla",
    link: Routes.NotFound.path
  },
  {
    id: 3,
    title: "Insightful reports",
    icon: faMobileAlt,
    description: "Blabla blabla blabla Blabla blabla blabla",
    link: Routes.NotFound.path
  }
];
