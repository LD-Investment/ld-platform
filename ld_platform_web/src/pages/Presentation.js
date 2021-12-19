import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheckCircle,
  faExternalLinkAlt,
  faMapMarkedAlt,
  faPager
} from "@fortawesome/free-solid-svg-icons";
import {
  faBootstrap,
  faReact,
  faSass
} from "@fortawesome/free-brands-svg-icons";
import {
  Button,
  Card,
  Col,
  Container,
  Image,
  ListGroup,
  Nav,
  Navbar,
  Row
} from "@themesberg/react-bootstrap";
import { Link } from "react-router-dom";
import { HashLink } from "react-router-hash-link";

import { Routes } from "../routes";
import MockupPresentation from "../assets/img/mockup-presentation.png";
import ReactHero from "../assets/img/technologies/react-hero-logo.svg";
import MapboxImg from "../assets/img/mockup-map-presentation.png";
import ReactMockupImg from "../assets/img/react-mockup.png";
import BS5IllustrationsImg from "../assets/img/illustrations/bs5-illustrations.svg";

import pages from "../data/pages";
import managers from "../data/managers";
import ProfileCover from "../assets/img/profile-cover.jpg";

export default () => {
  const PagePreview = props => {
    const { name, image, link } = props;
    return (
      <Col xs={6} className="mb-5">
        <Card.Link
          as={Link}
          to={link}
          className="page-preview page-preview-lg scale-up-hover-2"
        >
          <Image
            src={image}
            className="shadow-lg rounded scale"
            alt="Dashboard page preview"
          />

          <div className="text-center show-on-hover">
            <h6 className="m-0 text-center text-white">
              {name}{" "}
              <FontAwesomeIcon icon={faExternalLinkAlt} className="ms-2" />
            </h6>
          </div>
        </Card.Link>
      </Col>
    );
  };

  const ProfileCardWidget = props => {
    const { image, title, subtitle, text } = props;
    return (
      <Col xs={4} className="mb-5">
        <Card border="light" className="text-center p-0 mb-4">
          <div
            style={{ backgroundImage: `url(${ProfileCover})` }}
            className="profile-cover rounded-top"
          />
          <Card.Body className="pb-5">
            <Card.Img
              src={image}
              className="user-avatar large-avatar rounded-circle mx-auto mt-n7 mb-4"
            />
            <Card.Title>{title}</Card.Title>
            <Card.Subtitle className="fw-normal">{subtitle}</Card.Subtitle>
            <Card.Text className="text-gray mb-4">{text}</Card.Text>
          </Card.Body>
        </Card>
      </Col>
    );
  };

  return (
    <>
      <Navbar
        variant="dark"
        expand="lg"
        bg="dark"
        className="navbar-transparent navbar-theme-primary sticky-top"
      >
        <Container className="position-relative justify-content-between px-3">
          <Navbar.Brand
            as={HashLink}
            to="#home"
            className="me-lg-3 d-flex align-items-center"
          >
            <Image src={ReactHero} />
            <span className="ms-2 brand-text d-none d-md-inline">
              L&D Investment
            </span>
          </Navbar.Brand>

          <div className="d-flex align-items-center">
            <Navbar.Collapse id="navbar-default-primary">
              <Nav className="navbar-nav-hover align-items-lg-center">
                <Nav.Link as={HashLink} to="#who-are-we">
                  Who are we?
                </Nav.Link>
                <Nav.Link as={HashLink} to="#funds-and-bots">
                  Funds & Bots
                </Nav.Link>
                <Nav.Link
                  as={HashLink}
                  to="#ld-managers"
                  className="d-sm-none d-xl-inline"
                >
                  Managers
                </Nav.Link>
                <Nav.Link as={HashLink} to="#subscribe">
                  Subscribe
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
            <Button
              variant="secondary"
              as={Link}
              to={Routes.DashboardOverview.path}
              className="text-dark me-3"
            >
              L&D Platform{" "}
              <FontAwesomeIcon
                icon={faExternalLinkAlt}
                className="d-none d-sm-inline ms-1"
              />
            </Button>
          </div>
        </Container>
      </Navbar>
      <section
        className="section-header overflow-hidden pt-5 pt-lg-6 pb-9 pb-lg-12 bg-primary text-white"
        id="home"
      >
        <Container>
          <Row>
            <Col xs={12} className="text-center">
              <div className="react-big-icon d-none d-lg-block">
                <span className="fab fa-react" />
              </div>
              <h1 className="fw-bolder text-secondary">
                L&D Investment Platform
              </h1>
              <pre className="text-muted fw-light mb-5 h5">
                <span className="fw-bold">DeFi</span> powered{" "}
                <span className="fw-bold">hedge funds</span> &{" "}
                <span className="fw-bold">bots</span>
                <p>for traders, analysts and investors of web2.0 and 3.0</p>
              </pre>
              <div className="d-flex justify-content-center flex-column mb-6 mb-lg-5 mt-5" />
            </Col>
          </Row>
          <figure className="position-absolute bottom-0 left-0 w-100 d-none d-md-block mb-n2">
            <svg
              className="fill-soft"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 3000 185.4"
            >
              <path d="M3000,0v185.4H0V0c496.4,115.6,996.4,173.4,1500,173.4S2503.6,115.6,3000,0z" />
            </svg>
          </figure>
        </Container>
      </section>
      <div className="section pt-0">
        <Container className="mt-n10 mt-lg-n12 z-2">
          <Row className="justify-content-center">
            <Col xs={12}>
              {/* TODO: Change this mockup */}
              <Image src={MockupPresentation} alt="Mockup presentation" />
            </Col>
          </Row>
          <Row className="justify-content-center mt-5 mt-lg-6" id="who-are-we">
            <Col xs={6} md={3} className="text-center mb-4">
              <div className="icon icon-shape icon-lg bg-white shadow-lg border-light rounded-circle mb-4">
                <FontAwesomeIcon icon={faReact} className="text-secondary" />
              </div>
              <h3 className="fw-bolder">Ultimate Strategies</h3>
              <p className="text-gray">
                Ai-driven automatic bots that make a best decision regardless of
                market condition. Developed by world class quantitative
                researchers.
              </p>
            </Col>
            <Col xs={6} md={3} className="text-center">
              <div className="icon icon-shape icon-lg bg-white shadow-lg border-light rounded-circle mb-4">
                <FontAwesomeIcon icon={faSass} className="text-secondary" />
              </div>
              <h3 className="fw-bolder">Trustless Operations</h3>
              <p className="text-gray">
                A scalping bot that helps traders to execute trades by providing
                high, performant methods. Customizable to mock top-class
                traders.
              </p>
            </Col>
            <Col xs={6} md={3} className="text-center mb-4">
              <div className="icon icon-shape icon-lg bg-white shadow-lg border-light rounded-circle mb-4">
                <FontAwesomeIcon icon={faPager} className="text-secondary" />
              </div>
              <h3 className="fw-bolder">Reports to Funds</h3>
              <p className="text-gray">
                Live-streaming of investment indicators that foster decision
                powered by AI-driven predicative models like crypto news.
              </p>
            </Col>
            <Col xs={6} md={3} className="text-center">
              <div className="icon icon-shape icon-lg bg-white shadow-lg border-light rounded-circle mb-4">
                <FontAwesomeIcon
                  color="secondary"
                  icon={faBootstrap}
                  className="text-secondary"
                />
              </div>
              <h3 className="fw-bolder">Assets in Web2.0/3.0</h3>
              <p className="text-gray">
                Web2.0/3.0 focused investment reports that are streamed to
                subscibers in real-time researched by world top-class experts
              </p>
            </Col>
          </Row>
        </Container>
      </div>
      <section className="section section-md bg-soft pt-lg-3">
        <Container>
          <Row className="justify-content-between align-items-center mb-5 mb-lg-7">
            <Col lg={5} className="order-lg-2 mb-5 mb-lg-0">
              <h2>Powered by DeFi</h2>
              <p className="mb-3 lead fw-bold">
                Trustless, immutable track-records executed by L&D investment
                bots and strategies
              </p>
              <p className="mb-4">
                When selecting funds and asset managerial bots, one cannot know
                whether the claimed track-records of each funds are not
                intentionally forged or opinionated. All of orders and yields
                performed by L&D Investment funds and bots are carved into DeFi
                on-chain, thus fostering trustfulness and immutability of
                investment results.
              </p>
              <Button
                href="https://www.investopedia.com/decentralized-finance-defi-5113835"
                variant="secondary"
                target="_blank"
              >
                What is DeFi?{" "}
                <FontAwesomeIcon icon={faExternalLinkAlt} className="ms-1" />
              </Button>
            </Col>
            <Col lg={6} className="order-lg-1">
              <Image src={ReactMockupImg} alt="Calendar Preview" />
            </Col>
          </Row>
          <Row className="justify-content-between align-items-center mb-5 mb-lg-7">
            <Col lg={5}>
              <h2>Market beating Strategies</h2>
              <p className="mb-3 lead fw-bold">
                A direct exposure to various strategies developed by world class
                AI/Quant researchers.
              </p>
              <p className="mb-4">
                blablablablablablablablablablablablablablablablablablablablab
                blablablablablablablablablablablablablablablablablablablablab
                blablablablablablablablablablablablablablablablablablablablab
              </p>
              <p className="mb-4">
                hellohello hello hellohellohello hello hellohellohello hello
                hellohellohello hello hellohellohello hello hellohellohello
                hello hello
              </p>
              {/* TODO: Replace path to AI/Quant strategy pages */}
              <Button
                as={Link}
                to={Routes.Forms.path}
                variant="secondary"
                className="mb-5 mb-lg-0"
                target="_blank"
              >
                <FontAwesomeIcon icon={faReact} className="me-1" />
                L&D AI/Quant Strategies
              </Button>
            </Col>
            <Col lg={6} className="rounded shadow pt-3">
              <Image
                src={MapboxImg}
                alt="MapBox Leaflet.js Custom Integration Mockup"
              />
            </Col>
          </Row>
          <Row className="justify-content-between align-items-center mb-5 mb-lg-7">
            <Col lg={5} className="order-lg-2 mb-5 mb-lg-0">
              <h2 className="d-flex align-items-center">
                High-end Investment Reports{" "}
              </h2>
              <p className="mb-3 lead fw-bold">
                Get validated, insightful reports from Web2.0/3.0 investment
                experts in country
              </p>
              <p className="mb-4">
                blablablablablablablablablablablablablablablablablablablablab
                blablablablablablablablablablablablablablablablablablablablab
                blablablablablablablablablablablablablablablablablablablablab
              </p>
              <Button
                href="https://demo.themesberg.com/volt-pro-react/#/map"
                className="me-3"
                variant="secondary"
                target="_blank"
              >
                <FontAwesomeIcon icon={faMapMarkedAlt} className="me-2" />{" "}
                Report example
              </Button>
            </Col>
            <Col lg={6} className="order-lg-1">
              <Image src={BS5IllustrationsImg} alt="Front pages overview" />
            </Col>
          </Row>
        </Container>
      </section>
      <section
        className="section section-lg bg-primary text-white"
        id="funds-and-bots"
      >
        <Container>
          <Row className="justify-content-center mb-5 mb-lg-6">
            <Col xs={12} className="text-center">
              <h2 className="fw-light mb-3">
                Profit from our <span className="fw-bold">market-beating</span>{" "}
                bots
              </h2>
              <p className="lead px-lg-8">
                Our funds and bots are beating the crypto market! Check out
                their amazing track-records that are immnutably on-chained in
                DeFi.
              </p>
            </Col>
          </Row>
          <Row className="mb-5">
            {pages.map(page => (
              <PagePreview key={`page-${page.id}`} {...page} />
            ))}
          </Row>
        </Container>
      </section>
      <section className="section section-lg line-bottom-soft" id="ld-managers">
        <Container>
          <Row className="justify-content-between mb-5 mb-lg-6">
            <Col xs={12} className="text-center">
              <h2 className="fw-light mb-3">
                Meet our <span className="fw-bold">superb</span> fund managers
              </h2>
              <p className="lead px-lg-8">
                All funds and bots operated by L&D Investment are the direct
                results of researches and development by world-class AI/Quant
                engineers and researchers.
              </p>
            </Col>
          </Row>
          <Row className="d-flex align-items-center">
            {managers.map(manager => (
              <ProfileCardWidget key={`manager-${manager.id}`} {...manager} />
            ))}
          </Row>
        </Container>
      </section>
      <section
        className="section section-lg bg-primary text-white"
        id="subscribe"
      >
        <Container>
          <Row className="d-flex align-items-center">
            <Col xs={12} lg={8}>
              <h2 className="fw-light mb-3">
                <span className="fw-bold">Subscribe</span> L&D funds and bots!
              </h2>
              <p className="lead mb-4 me-lg-6">
                See the list of funds and bots running in L&D Investment
                Platform. Look carefully each of their yields, track-records and
                affinity of your investment style. Pick one and you will not all
                set!
              </p>
            </Col>
            <Col xs={12} md={6} lg={4} className="mb-5 mb-lg-0">
              <Card border="light" className="p-4 py-5 mt-lg-n5">
                <Card.Header className="bg-white border-0 pb-0">
                  <span className="d-block">
                    <h2 className="text-primary fw-bold align-top">
                      L&D offers..
                    </h2>
                  </span>
                </Card.Header>
                <Card.Body>
                  <ListGroup className="list-group-flush price-list">
                    <ListGroup.Item className="bg-white border-0 ps-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      10+ AI driven bots
                    </ListGroup.Item>
                    <ListGroup.Item className="bg-white border-0 ps-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      20+ Indicator bots
                    </ListGroup.Item>
                    <ListGroup.Item className="bg-white border-0 ps-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      1 Scalping manual bot
                    </ListGroup.Item>
                    <ListGroup.Item className="bg-white border-0 ps-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      5+ Insight reports daily
                    </ListGroup.Item>
                    <ListGroup.Item className="bg-white border-0 ps-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      On-chained fund results
                    </ListGroup.Item>
                    <ListGroup.Item className="bg-white border-0 border-0 ps-0 pb-0">
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className="text-success me-2"
                      />{" "}
                      Premium Consulting
                    </ListGroup.Item>
                  </ListGroup>
                </Card.Body>
                <Button
                  variant="secondary"
                  as={Link}
                  to={Routes.DashboardOverview.path}
                  className="text-dark me-3"
                >
                  Go to L&D Platform!{" "}
                  <FontAwesomeIcon
                    icon={faExternalLinkAlt}
                    className="d-none d-sm-inline ms-1"
                  />
                </Button>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
      <section className="section section-lg bg-white" id="getting-started">
        <Container>
          <Row className="justify-content-center text-center mb-5">
            <Col xs={12}>
              <h2 className="fw-light mb-3">
                Get some <span className="fw-bold">sleep</span>.
              </h2>
              <p className="lead px-lg-8">
                Do not stay overnight because of the crushed crypto wallet. Just
                subscribe L&D funds and bots via Platform and you will now crush
                the market.
              </p>
            </Col>
          </Row>
        </Container>
      </section>
      <footer className="footer py-6 bg-dark text-white">
        <Container>
          <Row>
            <Col md={4}>
              <Navbar.Brand
                as={HashLink}
                to="#home"
                className="me-lg-3 mb-3 d-flex align-items-center"
              >
                <Image src={ReactHero} />
                <span className="ms-2 brand-text">L&D Investment</span>
              </Navbar.Brand>
              <p>
                We run DeFi powered hedge funds & bots for traders, analysts and
                investors of web2.0 and 3.0.
              </p>
            </Col>
            <Col xs={6} md={2} className="mb-5 mb-lg-0">
              <span className="h5">More info</span>
              <ul className="links-vertical mt-2">
                <li>
                  <Card.Link target="_blank" href="https://themesberg.com/blog">
                    Blog
                  </Card.Link>
                </li>
                <li>
                  <Card.Link
                    target="_blank"
                    href="https://themesberg.com/about"
                  >
                    About Us
                  </Card.Link>
                </li>
              </ul>
            </Col>
            <Col xs={6} md={2} className="mb-5 mb-lg-0">
              <span className="h5">Other</span>
              <ul className="links-vertical mt-2">
                <li>
                  <Card.Link
                    target="_blank"
                    href="https://themesberg.com/contact"
                  >
                    Contact Us
                  </Card.Link>
                </li>
                <li>
                  <Card.Link
                    target="_blank"
                    href="https://themesberg.com/licensing"
                  >
                    License
                  </Card.Link>
                </li>
              </ul>
            </Col>
            <Col xs={12} md={4} className="mb-5 mb-lg-0">
              <span className="h5 mb-3 d-block">Stay tuned</span>
              <form action="#">
                <div className="form-row mb-2">
                  <div className="col-12">
                    <input
                      type="email"
                      className="form-control mb-2"
                      placeholder="example@company.com"
                      name="email"
                      aria-label="Subscribe form"
                      required
                    />
                  </div>
                  <div className="col-12">
                    <button
                      type="submit"
                      className="btn btn-secondary text-dark shadow-soft btn-block"
                      data-loading-text="Sending"
                    >
                      <span>Submit</span>
                    </button>
                  </div>
                </div>
              </form>
              <p className="text-muted font-small m-0">
                We’ll never share your details. See our{" "}
                <Card.Link className="text-white" href="#">
                  Privacy Policy
                </Card.Link>
              </p>
            </Col>
          </Row>
          <hr className="bg-gray my-5" />
          <Row>
            <Col className="mb-md-2">
              <div
                className="d-flex text-center justify-content-center align-items-center"
                role="contentinfo"
              >
                <p className="font-weight-normal font-small mb-0">
                  Copyright © Luke and David Investment, Inc. 2021-
                  <span className="current-year">2022</span>. All rights
                  reserved.
                </p>
              </div>
            </Col>
          </Row>
        </Container>
      </footer>
    </>
  );
};
