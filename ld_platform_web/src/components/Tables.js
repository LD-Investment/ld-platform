import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faEdit,
  faEllipsisH,
  faEye,
  faTrashAlt
} from "@fortawesome/free-solid-svg-icons";
import {
  Button,
  ButtonGroup,
  Card,
  Dropdown,
  Table
} from "@themesberg/react-bootstrap";
import LdAxios from "../api/axios";

export const SubscribedBotTable = () => {
  const [subscribedBots, setSubscribedBots] = React.useState([]);
  React.useEffect(() => {
    LdAxios.get("/api/users/subscribed-bots/").then(response => {
      if (!response) return;
      setSubscribedBots(response.data.data);
    });
  }, []);

  const TableRow = props => {
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
          <Dropdown as={ButtonGroup}>
            <Dropdown.Toggle
              as={Button}
              split
              variant="link"
              className="text-dark m-0 p-0"
            >
              <span className="icon icon-sm">
                <FontAwesomeIcon icon={faEllipsisH} className="icon-dark" />
              </span>
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item>
                <FontAwesomeIcon icon={faEye} className="me-2" /> View Details
              </Dropdown.Item>
              <Dropdown.Item>
                <FontAwesomeIcon icon={faEdit} className="me-2" /> Edit
              </Dropdown.Item>
              <Dropdown.Item className="text-danger">
                <FontAwesomeIcon icon={faTrashAlt} className="me-2" /> Remove
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
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
              <TableRow key={`subscribed-bot-${index}`} {...item} />
            ))}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
};
