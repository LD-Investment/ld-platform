import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleLeft, faEnvelope } from "@fortawesome/free-solid-svg-icons";
import { Button, Card, Col, Container, Row } from "@themesberg/react-bootstrap";
import { Link } from "react-router-dom";

import { Routes } from "../../routes";
import BgImage from "../../assets/img/illustrations/signin.svg";

export default () => {
  return (
    <main>
      <section className="d-flex align-items-center my-5 mt-lg-6 mb-lg-5">
        <Container>
          <Row
            className="justify-content-center form-bg-image"
            style={{ backgroundImage: `url(${BgImage})` }}
          >
            <Col
              xs={12}
              className="d-flex align-items-center justify-content-center"
            >
              <div className="mb-4 mb-lg-0 bg-white shadow-soft border rounded border-light p-4 p-lg-5 w-100 fmxw-500">
                <div className="text-center text-md-center mb-5 mt-md-0">
                  <h1>
                    <FontAwesomeIcon icon={faEnvelope} className="me-2" />
                  </h1>
                  <h2 className="mb-4">Thank you for signing up!</h2>
                </div>

                <div className="text-center text-md-center mb-5 mt-md-0">
                  <h5>
                    To finish your signup, please check your email for a
                    verification link.
                  </h5>
                </div>

                <p className="text-center">
                  <Card.Link
                    as={Link}
                    to={Routes.PlatformDashboard.path}
                    className="text-gray-700"
                  >
                    <Button>
                      <FontAwesomeIcon icon={faAngleLeft} className="me-2" />{" "}
                      Back to home
                    </Button>
                  </Card.Link>
                </p>

                <div className="text-center text-md-center mb-5 mt-md-0">
                  If you have any issues,
                  <Card.Link
                    href="mailto:support@ld-investment.ai"
                    className="fw-bold"
                  >
                    {" contact us"}
                  </Card.Link>
                  .
                </div>
              </div>
            </Col>
          </Row>
        </Container>
      </section>
    </main>
  );
};
