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

      //Have user login to google account
      dispatch('initGapi').then(() => {
        gapi.auth2
          .getAuthInstance()
          .signIn()
          .then(() => {

            //Now get their id token from google given that sign in
            var token = null;
            try {
              token = gapi.auth2
                .getAuthInstance()
                .currentUser.get()
                .getAuthResponse().id_token;
            } catch (e) {
              reject();
            }
            if (!token)
              reject();
            
            //Now we actually sign them up on our backend using that token
            api
              .createUser(token)
              .then(res => {
                //Success! Get the profile and complete the login
                var profile = res.data.result;

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
          });
      });
    });
  },

  // backdoor Sign in for floryan
  debugProfSignIn({ dispatch, commit }) {
    console.log('backdoor signing in...');
    return new Promise((resolve, reject) => {
      // verify token with a backend server (identify user)
      dispatch('verifyToken', '12345')
        .then(profile => {
          // Gather settings
          axios
            .get(`${API_URL}/settings/?id_token=${profile.id_token}`)
            .then(response => {
              const settings = response.data.result;
              commit('settings/colorChange', settings.color, {
                root: true,
              });
              console.log('Completing signIn');
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

  // backdoor Sign in for dummy student
  debugStudSignIn({ dispatch, commit }) {
    console.log('backdoor signing in...');
    return new Promise((resolve, reject) => {
      // verify token with a backend server (identify user)
      dispatch('verifyToken', '54321')
        .then(profile => {
          // Gather settings
          axios
            .get(`${API_URL}/settings/?id_token=${profile.id_token}`)
            .then(response => {
              const settings = response.data.result;
              commit('settings/colorChange', settings.color, {
                root: true,
              });
              console.log('Completing signIn');
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
  verifyToken({ commit }, token=null) {
    console.log('verifying token and user...');

    return new Promise((resolve, reject) => {

      var reject = false;
      if(IN_PROD){
        console.log('Verifying through google (verifyToken)');
        try {
          token = gapi.auth2
            .getAuthInstance()
            .currentUser.get()
            .getAuthResponse().id_token;
        } catch (e) {
          reject = true;;
        }
        if (!token) {
          reject = true;
        } 
      }

      /* This is where the verification is taking place */
      // This is checking to see if they have an account, and if they do then seeing if they can login
      if(reject){
        reject();
      }
      else{
        axios
          .get(`${ API_URL }/students/?id_token=${token}`)
          .then(res => {
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
