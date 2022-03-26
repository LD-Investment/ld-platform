import React from "react";
import { Button, Card, Image, OverlayTrigger, Tooltip } from "@themesberg/react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDownload } from "@fortawesome/free-solid-svg-icons";
import BS5Logo from "../assets/img/technologies/bootstrap-5-logo.svg";
import ReactLogo from "../assets/img/technologies/react-logo.svg";
import LaravelLogo from "../assets/img/technologies/laravel-logo.svg";
import GitHubButton from "react-github-btn";

export default () => {
  return (
    <div>
      <Card className="theme-settings">
        <Card.Body className="pt-4">
          <Button className="theme-settings-close" variant="close" size="sm" aria-label="Close" onClick={() => { toggleSettings(false) }} />
          <div className="d-flex justify-content-between align-items-center mb-3">
            <p className="m-0 mb-1 me-3 fs-7">Made with open source <span role="img" aria-label="gratitude">💙</span></p>
            <GitHubButton href="https://github.com/themesberg/volt-react-dashboard" data-size="large" data-show-count="true" aria-label="Star themesberg/volt-react-dashboard on GitHub">Star</GitHubButton>
          </div>
          <Button href="https://themesberg.com/product/dashboard/volt-react" target="_blank" variant="primary" className="mb-3 w-100"><FontAwesomeIcon icon={faDownload} className="me-1" /> Download</Button>
          <p className="fs-7 text-gray-700 text-center">Available in the following technologies:</p>
          <div className="d-flex justify-content-center">
            <Card.Link href="https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard" target="_blank">
              <OverlayTrigger placement="top" trigger={['hover', 'focus']} overlay={<Tooltip>Bootstrap 5 · The most popular HTML, CSS, and JS library in the world.</Tooltip>}>
                <Image src={BS5Logo} className="image image-xs" />
              </OverlayTrigger>
            </Card.Link>

            <Card.Link href="https://themesberg.com/product/dashboard/volt-react" target="_blank">
              <OverlayTrigger placement="top" trigger={['hover', 'focus']} overlay={<Tooltip>React · A JavaScript library for building user interfaces.</Tooltip>}>
                <Image src={ReactLogo} className="image image-xs" />
              </OverlayTrigger>
            </Card.Link>

            <Card.Link href="https://themesberg.com/product/laravel/volt-admin-dashboard-template" target="_blank">
              <OverlayTrigger placement="top" trigger={['hover', 'focus']} overlay={<Tooltip>Laravel · Most popular PHP framework in the world.</Tooltip>}>
                <Image src={LaravelLogo} className="image image-xs" />
              </OverlayTrigger>
            </Card.Link>

          </div>
        </Card.Body>
      </Card>
    </div>
  );
};
