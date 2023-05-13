import AbstractApi from './abstract_api';

const BASE_URL    = 'http://localhost:8080/api';     // http://api.address.com/api

class Api extends AbstractApi {
  constructor() {
    super(BASE_URL);
  }
}

export default new Api();
