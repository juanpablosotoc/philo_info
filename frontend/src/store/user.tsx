import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type {UserState } from '../utils/types';
import { post, saveToken } from "../utils/http";

const initialState: UserState = {};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    login(state, action: PayloadAction<UserState>) {
      state.email = action.payload.email;
    },
    logout(state) {
      state.email = undefined;
    }
  },
});

const { login: login_, logout: logout_ } = userSlice.actions;
const reducer = userSlice.reducer;

async function login(email: string, password: string) {
    const resData = await post("users/login", false, {email, password});
    saveToken(resData.token);
    login_({email});
};

async function register(email: string, password: string) {
    const resData = await post("users/create_user", false, {email, password});
    saveToken(resData.token);
    login_({email});
};

async function logout() {
    logout_();
}

export { login, register, logout };
export default reducer;