import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExternalLinkAlt, faHeart } from "@fortawesome/free-solid-svg-icons";
import {
  Button,
  Card,
  Col,
  Form,
  InputGroup,
  Modal,
  ProgressBar,
  Row,
  Table,
  Spinner
} from "@themesberg/react-bootstrap";
import { toast } from "react-toastify";

import LdAxios from "../api/axios";
import { Link } from "react-router-dom";
import { Routes } from "../routes";
import Datetime from "react-datetime";
import { CalendarIcon } from "@heroicons/react/solid";
import moment from "moment-timezone";
import AccordionComponent from "./AccordionComponent";
import { CustomPagination } from "./Pagination";

export const SubscribedBotTable = () => {
  const [subscribedBots, setSubscribedBots] = React.useState([]);
  React.useEffect(() => {
    LdAxios.get("/api/users/subscribed-bots/").then(response => {
      if (!response) return;
      setSubscribedBots(response.data.data);
    });
  }, []);

  const SubscribedBotTableRow = props => {
    const {
      bot,
      subscribe_end_date,
      status,
      status_display,
      run_type_display
    } = props;
    const statusVariant =
      status === "active" // consult BE for symbol
        ? "success"
        : status === "inactive"
        ? "warning"
        : "primary";

    const BotPathDecider = bot_name => {
      if (bot_name === "News Tracker") {
        return Routes.NewsTrackerBot.path;
      }
      return Routes.NotFound.path;
    };

    return (
      <tr>
        <td>
          <span className="fw-normal">{bot.name_display}</span>
        </td>
        <td>
          <span className="fw-normal">{bot.type_display}</span>
        </td>

        <td>
          <span className="fw-normal">{subscribe_end_date}</span>
        </td>
        <td>
          <span className="fw-normal">{run_type_display}</span>
        </td>
        <td>
          <span className={`fw-normal text-${statusVariant}`}>
            {status_display}
          </span>
        </td>

        <td>
          <Button
            variant="secondary"
            as={Link}
            to={() => BotPathDecider(bot.name_display)}
            className="text-dark me-3"
          >
            Open{" "}
            <FontAwesomeIcon
              icon={faExternalLinkAlt}
              className="d-none d-sm-inline ms-1"
            />
          </Button>
        </td>
      </tr>
    );
  };

  return (
    <Card border="light" className="table-wrapper table-responsive shadow-sm">
      <Card.Body className="pt-0">
        <Table hover className="user-table align-items-center">
          <thead>
            <tr>
              <th className="border-bottom">Name</th>
              <th className="border-bottom">Type</th>
              <th className="border-bottom">Expires at</th>
              <th className="border-bottom">Run Type</th>
              <th className="border-bottom">Status</th>
            </tr>
          </thead>
          <tbody>
            {subscribedBots.map((item, index) => (
              <SubscribedBotTableRow
                key={`subscribed-bot-${index}`}
                {...item}
              />
            ))}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
};

export const NewsTrackerNewsTable = () => {
  const [showSelectModal, setShowSelectModal] = React.useState(false);
  const [totalPage, setTotalPage] = React.useState(0);
  const [pageNum, setPageNum] = React.useState(1);
  const [newsLists, setNewsLists] = React.useState([]);
  const [selectedAiModelName, setSelectedAiModelName] = React.useState(null);
  const [selectedStartDate, setSelectedStartDate] = React.useState(null);
  const [selectedEndDate, setSelectedEndDate] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const baseUrl = `/api/bots/indicator/news-tracker/ai-model/${selectedAiModelName}/calculate?page=${pageNum}`;

  React.useEffect(() => {
    if (!selectedAiModelName) return;
    setIsLoading(true);
    LdAxios.post(baseUrl, {
      start_date: selectedStartDate.toString(),
      end_date: selectedEndDate.toString()
    }).then(response => {
      setIsLoading(false);
      if (!response) return;
      setNewsLists(response.data.data.results);
      setTotalPage(
        response.data.data.count / response.data.data.results.length
      );
    });
  }, [selectedAiModelName, baseUrl, selectedStartDate, selectedEndDate]);

  const NewsTable = () => {
    const TableRow = props => {
      const { id, title, content, date, score } = props;
      return (
        <tr>
          <td>{date}</td>
          <td>
            <AccordionComponent
              data={[
                {
                  id: `news-tracker-accordian-${id}`,
                  eventKey: `news-tracker-accordian-${id}`,
                  title: title,
                  description: content
                }
              ]}
            />
          </td>
          <td>
            <Row className="d-flex align-items-center">
              <Col xs={12} xl={2} className="px-0">
                <small className="fw-bold">Bull: {score[0]}%</small>
              </Col>
              <Col xs={12} xl={10} className="px-0 px-xl-1">
                <ProgressBar
                  variant="danger"
                  className="progress-lg mb-0"
                  now={score[0]}
                  size="lg"
                  min={0}
                  max={1.0}
                />
              </Col>
              <Col xs={12} xl={2} className="px-0">
                <small className="fw-bold">Neutral: {score[1]}%</small>
              </Col>
              <Col xs={12} xl={10} className="px-0 px-xl-1">
                <ProgressBar
                  variant="dark"
                  className="progress-lg mb-0"
                  now={score[1]}
                  size="lg"
                  min={0}
                  max={1.0}
                />
              </Col>
              <Col xs={12} xl={2} className="px-0">
                <small className="fw-bold">Bear: {score[2]}%</small>
              </Col>
              <Col xs={12} xl={10} className="px-0 px-xl-1">
                <ProgressBar
                  variant="info"
                  className="progress-lg mb-0"
                  now={score[2]}
                  size="lg"
                  min={0}
                  max={1.0}
                />
              </Col>
            </Row>
          </td>
        </tr>
      );
    };
    return (
      <Card border="light" className="shadow-sm mb-4">
        <Card.Body className="pb-0">
          <Table
            responsive
            className="table-centered table-nowrap rounded mb-0"
          >
            <thead className="thead-light">
              <tr>
                <th className="border-0">Date</th>
                <th className="border-0">News</th>
                <th className="border-0">Score</th>
              </tr>
            </thead>
            <tbody>
              {newsLists.map(news => (
                // console.log(news)
                <TableRow key={`news-tracker-news-${news.id}`} {...news} />
              ))}
            </tbody>
          </Table>
        </Card.Body>
        <Card.Body>
          <CustomPagination
            withIcons={true}
            totalPages={totalPage}
            pageNum={pageNum}
            setPageNum={setPageNum}
          />
        </Card.Body>
      </Card>
    );
  };

  const SelectModal = props => {
    const { selectedModelName, selectedStartDate, selectedEndDate } = props;
    const [modelName, setModelName] = React.useState(selectedModelName);
    const [start, setStart] = React.useState(selectedStartDate);
    const [end, setEnd] = React.useState(selectedEndDate);
    const [aiModels, setAiModels] = React.useState([]);

    React.useEffect(() => {
      LdAxios.get("/api/bots/indicator/news-tracker/ai-model").then(
        response => {
          if (!response) return;
          setAiModels(response.data.data.models);
        }
      );
    }, []);

    const startDate = start
      ? moment(start).format("YYYY-MM-DD")
      : moment().format("YYYY-MM-DD");
    const endDate = end
      ? moment(end).endOf("day").format("YYYY-MM-DD")
      : moment().format("YYYY-MM-DD");

    const onConfirm = e => {
      e.preventDefault();
      if (!modelName) {
        toast.error("Please select AI model.");
        return;
      }
      // const finalStart = moment(startDate).toDate();
      // const finalEnd = moment(endDate).toDate();

      setSelectedAiModelName(modelName);
      setSelectedStartDate(startDate);
      setSelectedEndDate(endDate);
      setShowSelectModal(false);
    };
    const onHide = () => {
      setShowSelectModal(false);
    };

    return (
      <Modal as={Modal.Dialog} centered show={showSelectModal} onHide={onHide}>
        <Form className="modal-content">
          <Modal.Body>
            <Row>
              <Form.Group id="aiModel" className="mb-4">
                <Form.Label>Select AI Model</Form.Label>
                {aiModels.map(models => (
                  <Form.Check
                    key={`news-tracker-ai-model-${models.id}`}
                    defaultChecked={models.name === modelName}
                    type="radio"
                    label={models.name}
                    htmlFor={`news-tracker-ai-model-${models.id}`}
                    onClick={() => setModelName(models.name)}
                  />
                ))}
              </Form.Group>
              <Col xs={12} lg={6}>
                <Form.Group id="startDate">
                  <Form.Label>Select start date</Form.Label>
                  <Datetime
                    timeFormat={false}
                    onChange={setStart}
                    renderInput={(props, openCalendar) => (
                      <InputGroup>
                        <InputGroup.Text>
                          <CalendarIcon className="icon icon-xs" />
                        </InputGroup.Text>
                        <Form.Control
                          required
                          type="text"
                          placeholder="YYYY-MM-DD"
                          value={startDate}
                          onFocus={openCalendar}
                          onChange={() => {}}
                        />
                      </InputGroup>
                    )}
                  />
                </Form.Group>
              </Col>
              <Col xs={12} lg={6}>
                <Form.Group id="endDate" className="mb-2">
                  <Form.Label>Select end date</Form.Label>
                  <Datetime
                    timeFormat={false}
                    onChange={setEnd}
                    isValidDate={currDate => currDate.isAfter(start)}
                    renderInput={(props, openCalendar) => (
                      <InputGroup>
                        <Form.Control
                          required
                          type="text"
                          placeholder="YYYY-MM-DD"
                          value={endDate}
                          onFocus={openCalendar}
                          onChange={() => {}}
                        />
                      </InputGroup>
                    )}
                  />
                </Form.Group>
              </Col>
            </Row>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="primary" className="me-2" onClick={onConfirm}>
              Confirm
            </Button>
            <Button
              variant="link"
              className="text-gray ms-auto"
              onClick={onHide}
            >
              Close
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    );
  };

  return (
    <div>
      <div className="d-xl-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
        <Button
          variant="outline-primary"
          className="m-1"
          onClick={() => setShowSelectModal(true)}
        >
          <FontAwesomeIcon icon={faHeart} className="me-2" /> Apply Filter
        </Button>
      </div>
      <div>{isLoading ? <Spinner animation="border" /> : <NewsTable />}</div>
      <div>
        {showSelectModal ? (
          <SelectModal
            selectedModelName={selectedAiModelName}
            selectedStartDate={selectedStartDate}
            selectedEndDate={selectedEndDate}
          />
        ) : null}
      </div>
    </div>
  );
};
