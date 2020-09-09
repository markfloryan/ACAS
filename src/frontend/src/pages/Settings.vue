<template>
  <div class="Settings">
    <h2>Settings</h2>
    <div class="content">
      <h2 class="title">Personalize</h2>
      <div id="buttoncontainer">
        <!-- this button saves local color to global vuex store -->
        <button
          class="btn btn-primary"
          :style="returnPrimaryButtonStyle"
          v-on:click="updateSettings()"
          @click="sendSettings"
        >Update Color</button>
      </div>
      
      

      <!--here is where the vue color pallette is, and the function call to change local color -->
      <div class="settings-body">
        <div clqass="color-change">Profile Color:
          <compact id="for.css" v-model="colors" @input="setColor"/>
        </div>
        <br/>

        <router-link :to="'/'">
          <button class="create-class btn btn-create"  style="height:8%;width:10%;margin-top:5px;">
            Home
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters, mapMutations } from 'vuex';
import store from '../vuex';
import { Compact } from 'vue-color';
import axios from 'axios';
import { API_URL } from '@/constants';
//local color variable which changes the current color on this page
let placeholderColor = '#fff';
export default {
  name: 'Settings',

  components: {
    Compact,
  },

  data() {
    return {
      isProfessor: false,
      //color is a hex val, nickname will later be
      colors: '#FFFFFF',
      nickname: 'stuff',
      sites_and_courses: {},
      createGrade:{},
      updateGrade:{},
      deleteGrade:{}
    };
  },
  computed: {
    ...mapGetters('settings', [
      'returnColor',
      'returnNickName',
      'returnPrimaryButtonStyle',
    ]),
    ...mapState('auth', ['profile']),
  },
  mounted() {
    this.isProfessor = this.profile.is_professor;
  },
  methods: {

    currentColor() {
      return this.returnColor();
    },

    setColor(data) {
      //changes local color to the value sent from the color palette
      placeholderColor = data.hex;
    },

    updateSettings(data) {
      this.colorChange(placeholderColor);
      this.nicknameChange(this.nickname);
    },

    sendSettings() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      const data = {
        colors: this.colors,
        nickname: this.nickname,
      };
      //sends settings data to the students settings page.
      axios.put(`${API_URL}/settings/`, data, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then( (response) => {
          if (data && data.data && data.data.result) {
            const classData = data.data.result;
            this.classData = {
              uuid: classData.pk,
              color: classData.color,
              nickname: classData.name,
            };
          }
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Profile Color',
            message: 'Successfully updated settings',
            duration: 6000,
          });
        })
        .catch( (error) => {

          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Profile Color',
            message: 'Failed to update settings',
            duration: 6000,
          });
        })
        .finally(() => {
          this.isLoading = false;
        });

    },




    ...mapMutations(
      'toast',
      ['openToast', 'setToastInfo'],
    ),
    ...mapMutations(
      'settings',
      ['colorChange', 'nicknameChange'],
    ),
  }, // End of method
};
</script>








<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.Settings {
  height: 100%;
  width: 100%;
}
.content {
  font-size: 20pt;
  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 30pt;
  border-radius: 6pt;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}
.color-change {
  padding: 3%;
  height: 5%;
  font-size: 12.75pt;
  margin-top: 10pt;
}
#name-change {
  padding: 3%;
  height: 5%;
  font-size: 12.75pt;
  margin-top: 80pt;
}

#enter-name {
  float: right;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  border-radius: 3.75pt;
  width: 80%;
  padding: 3pt;
}
#photo {
  float: right;
}
#rightAlign {
  text-align: right;
  float: right;
}
#buttoncontainer {
  text-align: right;
  grid-area: buttoncontainer;
}
.Settings .title {
  grid-area: title;
}
.Settings .settings-body {
  grid-area: settingsBody;
}
.Settings .content {
  display: grid;
  grid-template-areas:
    'title buttoncontainer'
    'settingsBody settingsBody';
  grid-template-rows: min-content 1fr;
  grid-auto-columns: 1fr 1fr;
}
div#externalContent {
  font-size: 12pt;
  padding: 0% 0% 0% 5%;
  line-height: 2;
}
.externalContent {
  display: grid;
  grid-template-columns: 20% 40% 40%;
  font-size: 12pt;
  padding: 0% 0% 0% 5%;
  line-height: 2;
}
.colorGrid {
  display: grid;
  grid-template-columns: 70% 30%;
}
div#colorContainer-right{
  text-align: right;
}
.future-features{
  position: fixed;
  display: none;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  z-index: 2;
  cursor: pointer;
}
.prevent-action-overlay {
  height: 100%;
  width: 100%;
  background-color: rgba(20, 20, 20, 0.5);
  position: absolute;
  top: 0;
  left: 0;
}
</style>
