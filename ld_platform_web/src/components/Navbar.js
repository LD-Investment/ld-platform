import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSignOutAlt } from "@fortawesome/free-solid-svg-icons";
import { observer } from "mobx-react";
import useUserStore, { userStore } from "../store/user_store_context";
import {
  Container,
  Dropdown,
  Image,
  Nav,
  Navbar
} from "@themesberg/react-bootstrap";

import EmptyProfilePicture from "../assets/img/team/profile-picture-empty.jpg";
import LdAxios from "ld-axios/axios";

const handleLogOut = () => {
  LdAxios.get("/api/auth/logout/").then(() => {
    userStore.resetUserInfo();
    window.location.reload();
  });
};

const UserInfoNavBar = observer(() => {
  const userStore = useUserStore();
  return (
    <Navbar variant="dark" expanded className="ps-0 pe-2 pb-0">
      <Container fluid className="px-0">
        <div className="d-flex justify-content-between w-100">
          <div className="d-flex align-items-center" />
          <Nav className="align-items-center">
            <Dropdown as={Nav.Item}>
              <Dropdown.Toggle as={Nav.Link} className="pt-1 px-0">
                <div className="media d-flex align-items-center">
                  <Image
                    src={EmptyProfilePicture}
                    className="user-avatar md-avatar rounded-circle"
                  />
                  <div className="media-body ms-2 text-dark align-items-center d-none d-lg-block">
                    <span className="mb-0 font-small fw-bold">
                      {userStore.userInfo.username}
                    </span>
                  </div>
                </div>
              </Dropdown.Toggle>
              <Dropdown.Menu className="user-dropdown dropdown-menu-right mt-2">
                <Dropdown.Item className="fw-bold" onClick={handleLogOut}>
                  <FontAwesomeIcon
                    icon={faSignOutAlt}
                    className="text-danger me-2"
                  />{" "}
                  Logout
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Nav>
        </div>
      </Container>
    </Navbar>
  );
});

export default UserInfoNavBar;
