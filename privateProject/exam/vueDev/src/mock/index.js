import { createProdMockServer } from "vite-plugin-mock/client";
import MockMethod from "./api.js";


export function setupProdMockServer() {
    createProdMockServer([...MockMethod]);
}
