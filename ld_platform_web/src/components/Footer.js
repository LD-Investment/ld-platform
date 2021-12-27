import React from "react";
import moment from "moment-timezone";
import { Card, Col, Row } from "@themesberg/react-bootstrap";

export default props => {
  const currentYear = moment().get("year");
  return (
    <div>
      <footer className="footer section py-5">
        <Row>
          <Col xs={12} lg={6} className="mb-4 mb-lg-0">
            <p className="mb-0 text-center text-xl-left">
              Copyright © 2021-{`${currentYear} `}
              {/* TODO: Change with real site url */}
              <Card.Link
                href="https://localhost:9000"
                target="_blank"
                className="text-blue text-decoration-none fw-normal"
              >
                L&D Investment
              </Card.Link>
            </p>
          </Col>
        </Row>
      </footer>
    </div>
  );
};
