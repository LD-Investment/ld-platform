import { action, computed, makeObservable, observable } from "mobx";
import { createContext, useContext } from "react";
import LdAxios from "ld-axios/axios";

export class UserStore {
  userInfo = {
    username: "",
    email: "",
    firstName: "",
    lastName: ""
  };
  constructor() {
    makeObservable(this);
  }

  get isUserInfoEmpty() {
    return this.userInfo.username === "" || this.userInfo.email === "";
  }

  initUserInfo = data => {
    this.userInfo = {
      username: data.username,
      email: data.email,
      firstName: data.first_name,
      lastName: data.last_name
    };
  };

  updateUserInfo = () => {
    LdAxios.get("/api/users/profile/").then(res => {
      if (res) {
        this.initUserInfo(res.data.data);
      }
    });
  };

  resetUserInfo = () => {
    this.userInfo = {
      username: "",
      email: "",
      firstName: "",
      lastName: ""
    };
  };
}

export const userStore = new UserStore();
const UserStoreContext = createContext(userStore);

const useUserStore = () => {
  return useContext(UserStoreContext);
};

export default useUserStore;
