import React from "react";
import { Image } from "@themesberg/react-bootstrap";

import LDGradient3DLogo from "../assets/img/logo/logo_gradient_3d.png";

export default props => {
  const { show } = props;

  return (
    <div
      className={`preloader bg-soft flex-column justify-content-center align-items-center ${
        show ? "" : "show"
      }`}
    >
      <Image
        className="loader-element animate__animated animate__jackInTheBox"
        src={LDGradient3DLogo}
        height={40}
      />
    </div>
  );
};
