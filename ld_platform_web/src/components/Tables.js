import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons";
import { Button, Card, Table } from "@themesberg/react-bootstrap";
import LdAxios from "../api/axios";
import { Link } from "react-router-dom";
import { Routes } from "../routes";

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
      status === "ACTV" // consult BE for symbol
        ? "success"
        : status === "INAC"
        ? "warning"
        : "primary";

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
            to={Routes.NotFound.path}
            className="text-dark me-3"
          >
            Control{" "}
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
