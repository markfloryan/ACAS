import api from '../../api';
import store from '../index';
import axios from 'axios';
import { API_URL } from '@/constants/';
import { DEBUG_TOKEN } from '@/constants/';
//import { IN_PROD } from '@/constants/';

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
          gapi.auth2 // Note: apply_deployment_vars.sh will update the client_id when during the production docker build
            .init({  // The script will break if the client_id string is changed such that it is no longer on its own line.
              client_id: '250281465409-dohlj94rioi60eiqqc2mdmsh4klgcpck.apps.googleusercontent.com', // You can change the string itself
            }) // But do not put this closing curly brace and parenthesis on the same line as the client_id or else the production build will break
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


                var data = {};

                // Create their settings
                axios
                  .post(`${API_URL}/settings/`, data, { headers: { Authorization: `Bearer ${profile.id_token}` } })
                  .then(response => {
                    //Created settings
                  })
                  .catch(response => {
                    //Error creating settings
                  })
                  .finally(() => {
                    if(profile.is_professor == 'f'){
                      profile.is_professor = false;
                    }
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

  // Sign in a user
  signIn({ dispatch, commit }) {
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
                  .get(`${API_URL}/settings/`, { headers: { Authorization: `Bearer ${profile.id_token}` } })
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

    return new Promise((resolve, reject) => {

      var reject = false;
      try {
        token = gapi.auth2
          .getAuthInstance()
          .currentUser.get()
          .getAuthResponse().id_token;
      } catch (e) {
        reject = true;
      }	
      if (!token) {
        reject = true;
      } 
      

      /* This is where the verification is taking place */
      // This is checking to see if they have an account, and if they do then seeing if they can login
      if(!reject){
        axios
          .get(`${ API_URL }/students/`, { headers: { Authorization: `Bearer ${token}` } })
          .then(res => {
            resolve(res.data.result);
          })
          .catch(err => {
            // https://gist.github.com/fgilio/230ccd514e9381fafa51608fcf137253
            if (err.response) {
              if (err.response.status == 404 || err.response.status == 403) {
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
