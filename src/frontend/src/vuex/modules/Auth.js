import api from '../../api';
import store from '../index';
import axios from 'axios';
import { API_URL } from '@/constants/';
import { IN_PROD } from '@/constants/';
import { DEBUG_TOKEN } from '@/constants/';

const state = {
  signedIn: false,
  profile: null,
};

const actions = {
  // Contact the google API
  initGapi({ commit }) {
    return new Promise((resolve, reject) => {
      gapi.load('auth2', {
        callback: () => {
          gapi.auth2
            .init({
              client_id:
                '154866204116-qc30nu7lvle8isniqmrhnuhers4g12g2.apps.googleusercontent.com',
            })
            .then(() => {
              resolve();
            });
        },
      });
    });
  },
  // See if a user is signed in
  isSignedIn({ dispatch, commit, state }) {
    return new Promise((resolve, reject) => {
      dispatch('initGapi').then(() => {
        var currentUser = null;
        try {
          currentUser = gapi.auth2.getAuthInstance().currentUser.get();
        } catch (e) {
          resolve(false);
        }

        // not signed in - delete persisted user
        if (!currentUser) {
          commit('signOut');
          resolve(false);
        }
        // persisted user id same with signed in google user's id
        if (state.profile && state.profile.sub === currentUser.getId()) {
          commit('signIn');
          resolve(true);
        }
        // persisted user id different with signed in google user's id
        else {
          dispatch('signOut').then(() => {
            resolve(false);
          });
        }
      });
    });
  },
  // Sign a user up
  signUp({ dispatch, commit }, isProfessor) {
    console.log('signing up... ');
    return new Promise((resolve, reject) => {
      dispatch('initGapi').then(() => {
        gapi.auth2
          .getAuthInstance()
          .signIn()
          .then(() => {
            // Student case
            if (!isProfessor) {
              // verify token with a backend server (identify user)
              dispatch('signUpUser')
                .then(profile => {
                  console.log({ profile });
                  const data = {
                    token: profile.id_token,
                  };
                  // Retrieve their settings
                  axios
                    .post(`${API_URL}/settings/`, data)
                    .then(response => {
                      console.log('CREATED SETTINGS');
                    })
                    .catch(response => {
                      console.log('ERROR CREATING SETTINGS');
                    })
                    .finally(() => {
                      console.log('FINALLY SETTINGS');
                      commit('signIn', profile);
                      resolve();
                    });
                })
                // if an error exists, log them out
                .catch(err => {
                  console.log(err);
                  dispatch('signOut').then(() => {
                    reject();
                  });
                });
            }
            // professor case
            else {
              // verify token with a backend server (identify user)
              dispatch('signUpProfessor')
                .then(profile => {
                  console.log({ profile });
                  const data = {
                    token: profile.id_token,
                  };
                  axios
                    .post(`${API_URL}/settings/`, data)
                    .then(repsonse => {})
                    .catch(response => {})
                    .finally(() => {
                      commit('signIn', profile);
                      resolve();
                    });
                })
                .catch(err => {
                  console.log(err);
                  dispatch('signOut').then(() => {
                    reject();
                  });
                });
            }
          });
      });
    });
  },

  // backdoor Sign in for floryan
  debugSignIn({ dispatch, commit }) {
    console.log('backdoor signing in...');
    return new Promise((resolve, reject) => {
      // verify token with a backend server (identify user)
      dispatch('verifyToken')
        .then(profile => {
          // Gather settings
          axios
            .get(`${API_URL}/settings/?id_token=${profile.id_token}`)
            .then(response => {
              const settings = response.data.result;
              commit('settings/colorChange', settings.color, {
                root: true,
              });
              console.log("Completing signIn");
              commit('signIn', profile);
              resolve();
            })
            .catch(response => {});
        })
        .catch(err => {
          console.log(err);
          dispatch('signOut').then(() => {
            reject();
          });
        });
    });
  },

  // Sign in a user
  signIn({ dispatch, commit }) {
    console.log('signing in...');
    return new Promise((resolve, reject) => {
      dispatch('initGapi').then(() => {
        // Reach out to google and get current user
        gapi.auth2
          .getAuthInstance()
          .signIn()
          .then(() => {
            // verify token with a backend server (identify user)
            dispatch('verifyToken')
              .then(profile => {
                // Gather settings
                axios
                  .get(`${API_URL}/settings/?id_token=${profile.id_token}`)
                  .then(response => {
                    const settings = response.data.result;
                    commit('settings/colorChange', settings.color, {
                      root: true,
                    });
                    commit('signIn', profile);
                    resolve();
                  })
                  .catch(response => {});
              })
              .catch(err => {
                console.log(err);
                dispatch('signOut').then(() => {
                  reject();
                });
              });
          });
      });
    });
  },
  // Sign a user out
  signOut({ commit }) {
    console.log('signing out...');
    return new Promise((resolve, reject) => {
      if (gapi && gapi.auth2 && gapi.auth2.getAuthInstance()) {
        gapi.auth2
          .getAuthInstance()
          .signOut()
          .then(
            () => {
              commit('signOut');
              resolve();
            },
            () => {
              commit('signOut');
              resolve();
            }
          );
      } else {
        commit('signOut');
        resolve();
      }
    });
  },
  // This action verifies the id_token parameter with a backend
  // server and receives the user profile as response
  signUpUser({ commit }) {
    console.log('verifying token and creating user...');
    return new Promise((resolve, reject) => {
      var token = null;
      try {
        token = gapi.auth2
          .getAuthInstance()
          .currentUser.get()
          .getAuthResponse().id_token;
      } catch (e) {
        reject();
      }
      if (!token) {
        reject();
      } else {
        /* This is where the verification is taking place */
        // We actually want to save the id_token, not the unique part
        api
          .createUser(token, true, false)
          .then(res => {
            console.log(res.data.result);
            resolve(res.data.result);
          })
          .catch(err => {
            // https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253

            // Custom toasts for errors from google and functions to logging in
            if (err.response) {
              if (err.response.status == 404) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'User does not exist',
                });
              }
              if (err.response.status == 400) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Bad Request',
                });
              }
              if (err.response.status == 500) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Internal Server Error',
                });
              }
            }
          });
      }
    });
  },
  signUpProfessor({ commit }) {
    console.log('verifying token and creating user...');
    return new Promise((resolve, reject) => {
      var token = null;
      try {
        token = gapi.auth2
          .getAuthInstance()
          .currentUser.get()
          .getAuthResponse().id_token;
      } catch (e) {
        reject();
      }
      if (!token) {
        reject();
      } else {
        /* This is where the verification is taking place */
        // We actually want to save the id_token, not the unique part
        api
          .createUser(token, true, true)
          .then(res => {
            console.log(res.data.result);
            resolve(res.data.result);
          })
          .catch(err => {
            // https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253

            // Custom toasts for errors from google and functions to logging in
            if (err.response) {
              if (err.response.status == 404) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'User does not exist',
                });
              }
              if (err.response.status == 400) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Bad Request',
                });
              }
              if (err.response.status == 500) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Internal Server Error',
                });
              }
            }
          });
      }
    });
  },
  // This action verifies the id_token parameter with a backend
  // server and receives the user profile as response
  verifyToken({ commit }) {
    console.log('verifying token and user...');

    return new Promise((resolve, reject) => {

      var token = null;
      var reject = false;
      if(!IN_PROD){
        console.log("Setting token to debug value");
        token = DEBUG_TOKEN;
      }
      else{
        console.log("Verifying through google (verifyToken)");
        try {
          token = gapi.auth2
            .getAuthInstance()
            .currentUser.get()
            .getAuthResponse().id_token;
        } catch (e) {
          console.log("Caught: Setting reject to true");
          reject = true;;
        }
        if (!token) {
          console.log("token is null, setting reject to true");
          reject = true;
        } 
      }

      /* This is where the verification is taking place */
      // This is checking to see if they have an account, and if they do then seeing if they can login
      if(reject){
        console.log("reject is true in verifyToken");
        reject();
      }
      else{
        api
          .createUser(token, false)
          .then(res => {
            console.log("Got profile back 2: ");
            console.log(res.data.result);
            resolve(res.data.result);
          })
          .catch(err => {
            // https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253
            if (err.response) {
              if (err.response.status == 404) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'User does not exist',
                });
              }
              if (err.response.status == 400) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Bad Request',
                });
              }
              if (err.response.status == 500) {
                store.commit('toast/openToast', true);
                store.commit('toast/setToastInfo', {
                  type: 'error',
                  title: 'Internal Server Error',
                });
              }
            }
          });
      }
    });
  },
};

const mutations = {
  signIn(state, profile) {
    
    state.signedIn = true;
    if (profile) {
      state.profile = profile;
    }
  },
  signOut(state) {
    state.signedIn = false;
    state.profile = null;
  },
};

const getters = {
  isSignedIn: state => {
    return state.signedIn;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters,
};
