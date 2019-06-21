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

        <!-- Is Professor? -->
        <div class="rightAlign" v-if="this.profile.group == 1">
          <h2 style="display:inline;"> External API's </h2>
          <span style="float:right;">
            <button
                class="btn btn-primary"
                :style="returnPrimaryButtonStyle"
                v-on:click="putExternalSiteList()"
                title="External Sites List"
              > Update API's </button>
          </span>

          <div v-for="site in externalSiteList" :key="site.pk">
            <label>{{ site.website_name }}</label>
            <input type="checkbox" :value="site.pk" v-model="checkedSitesList" >
            <br/>
          </div>

          <!-- <div id="colorContainer-right">
            this button saves local color to global vuex store
            <button
              class="btn btn-primary"
              :style="returnPrimaryButtonStyle"
              v-on:click="updateSettings()"
              @click="sendSettings"
            >Save Color</button>
          </div> -->
        </div>
        <br/>

        
        <!-- Is Professor? -->
        <div class="rightAlign" v-if="this.profile.group == 1">
   
          <h4 class="rightAlign" style="font-style: italic; text-align: right;">These features coming soon</h4>
          <div style="position: relative;">
              <div class="prevent-action-overlay"></div>
              <!-- Create External Grades -->
              <div id="createExternalGrades">
                <h2> Create External Grades </h2>

                <div class="externalContent" id="externalContent">
                  <span>
                    <label>Site: </label>
                  </span>
                  <span>
                    <select id="createExternalGrades-site" v-on:change="createExternalGrades_changeSite()">
                      <option v-for="(site, indexSite) in sites_and_courses.sites" :key="indexSite" :value="indexSite"> 
                        {{site.name}}({{site.base_url}})
                      </option>
                    </select>
                  </span>
                  <span>
                  </span>

                  <span>
                    <label>Course: </label>
                  </span>
                  <span>
                    <select id="createExternalGrades-course" >
                      <option v-for="(course, indexCourse) in sites_and_courses.courses" :key="indexCourse" :value="indexCourse"> 
                        {{course.name}}
                      </option>
                    </select>
                  </span>
                  <span>
                  </span>

                  <span>
                    <label>URL Ending: </label>
                  </span>
                  <span>
                    <input type="text" id="createExternalGrades-url_ending" v-model="createGrade.url_ending" autocomplete="off"/>
                  </span>
                  <span style="text-align: right;">
                    <button class="btn btn-primary" 
                      :style="returnPrimaryButtonStyle" v-on:click="createExternalGrades_button()"> Create </button>
                  </span>
                </div>
                <div id="externalContent">
                  <p><i> {{createGrade && createGrade.site ? createGrade.site.base_url : null }}{{ createGrade ? createGrade.url_ending : null }} </i></p>
                </div>
              </div>
              <br/>

            
              <!-- Update External Grades -->
              <div id="updateExternalGrades">
                <h2> Update External Grades </h2>

                <div class="externalContent"  id="externalContent">


                  <span>
                    <label>Course: </label>
                  </span>
                  <span>
                    <select id="updateExternalGrades-course" v-on:change="updateExternalGrades_changeCourse()" >
                      <option v-for="(course, indexCourse) in sites_and_courses.courses" :key="indexCourse" :value="indexCourse"> 
                        {{course.name}}
                      </option>
                    </select>
                  </span>
                  <span>
                  </span>

                  <span>
                    <label>Site: </label>
                  </span>
                  <span>
                    <select id="updateExternalGrades-site" >
                      <option v-for="(site, indexSite) in updateGrade.sites" :key="indexSite" :value="indexSite"> 
                        {{site.name}}({{site.url}})
                      </option>
                    </select>
                  </span>
                  <span style="text-align: right;">
                    <button class="btn btn-primary" 
                      :style="returnPrimaryButtonStyle" v-on:click="updateExternalGrades_button()">  Update </button>
                  </span>

                </div>
              </div>
              <br/>
          </div>
          


          <!-- Delete External Grades -->
          <div id="deleteExternalGrades">
            <h2> Delete External Grades </h2>

            <div class="externalContent"  id="externalContent">
              <span>
                <label>Course: </label>
              </span>
              <span>
                <select id="deleteExternalGrades-course" v-on:change="deleteExternalGrades_changeCourse()" >
                  <option v-for="(course, indexCourse) in sites_and_courses.courses" :key="indexCourse" :value="indexCourse"> 
                    {{course.name}}
                  </option>
                </select>
              </span>
              <span>
              </span>

              <span>
                <label>Site: </label>
              </span>
              <span>
                <select id="deleteExternalGrades-site" >
                  <option v-for="(site, indexSite) in deleteGrade.sites" :key="indexSite" :value="indexSite"> 
                    {{site ? site.name : null }}({{ site ? site.url : null }})
                  </option>
                </select>
              </span>
              <span style="text-align: right;">
                <button class="btn btn-primary" 
                  :style="returnPrimaryButtonStyle" v-on:click="deleteExternalGrades_button()">  Delete </button>
              </span>
            </div>
          </div>

        </div>
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
    this.isProfessor = this.profile.group;
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
        token: profile.auth.profile.id_token,
      };
      //sends settings data to the students settings page.
      axios.put(`${API_URL}/settings/`, data)
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

    /********************************************************************************   Get - SitesAndCourses
      getSitesAndCourses: Gets all External API' for SPT and Courses for Professor 

      this.sites_and_courses= {
        sites: [{name:'', base_url:'',pk:1}],
        courses: [{name: 'CS 2150', pk: 1}],
      };
    ********************************************************************************/
    async getSitesAndCourses(){
      const profile = JSON.parse(localStorage.getItem('profile'));
      
      

      let sites = [];


      // Get ExternalSites approved API
      await axios.get(`${API_URL}/external_sites/?id=${profile.auth.profile.id_token}`)
        .then((response)=> {
          sites = response.data.result;
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'External Grade Error',
            message: 'HEY',
            duration: 6000, 
          });
        })
        .finally(() => {
        });

      let courses = [];
      // Get Courses for professor
      await axios.get(`${API_URL}/student/course/?id_token=${profile.auth.profile.id_token}`)
        .then((response)=> {
          const studentToCourses = response.data.result;

          studentToCourses.forEach((studentToCourse)=>{
            let course = {
              name: String(studentToCourse.course.subject_code) + ' ' + String(studentToCourse.course.course_code),
              pk: studentToCourse.course.id 
            };


            courses.push(course);

          });
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'External Grade Error',
            message: 'Can\'t courses for professor',
            duration: 6000, 
          });
        })
        .finally(() => {
        });

      this.sites_and_courses= {
        sites: sites,
        courses: courses,
      };


      if ((this.sites_and_courses.sites) && (this.sites_and_courses.courses)){
        this.createGrade = {site: this.sites_and_courses.sites[0], course: this.sites_and_courses.courses[0], url_ending: ''};
      }
      else if (this.sites_and_courses.sites){
        this.createGrade = {site: this.sites_and_courses.sites[0], course: [], url_ending: ''};
      }
      else if (this.sites_and_courses.courses){
        this.createGrade = {site: [], course: this.sites_and_courses.courses[0], url_ending: ''};
      }

      if (this.sites_and_courses.courses) {      
        // Get External Site For Selected Course
        let course_pk = this.sites_and_courses.courses[0].pk;
        let sites = [];
        await axios.get(`${API_URL}/external_sites_to_course/${course_pk}?id=${profile.auth.profile.id_token}`)
          .then((response)=> {
            let externalSitesToCourse = response.data.result;
            
            // If single object, function as an array
            if ( !Array.isArray(externalSitesToCourse) )  {
              externalSitesToCourse = [ externalSitesToCourse ];
            }
            

            externalSitesToCourse.forEach((externalSiteToCourse)=>{
              let site = {
                name: String(externalSiteToCourse.external_site.name) ,
                url: String(externalSiteToCourse.external_site.base_url) + String(externalSiteToCourse.url_ending),
                externalSite_pk: externalSiteToCourse.external_site.id, 
                externalSiteToCourse_pk: externalSiteToCourse.pk
              };
              sites.push(site);
            });

            this.deleteGrade={sites: sites,course_index: 0};
            this.updateGrade= {sites: sites,course_index: 0};
          })
          .catch((error) => {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'External Grade Error',
              message: 'Can\'t get associated sites to course',
              duration: 6000, 
            });
          });
      }
      else {
        this.deleteGrade={sites:[],course_index: 0};
        this.updateGrade= {sites:[],course_index: 0};

      }

      

    },



      


    /********************************************************************************   CreateExternalGrades - ChangeSite
      createExternalGrades_changeSite: Changes the base_url based on dropdown
    ********************************************************************************/
    async createExternalGrades_changeSite(){
      let site_index = document.getElementById('createExternalGrades-site').value;
      this.createGrade.site = this.sites_and_courses.sites[site_index];
    },
    /********************************************************************************   CreateExternalGrades - Button
      createExternalGrades_button: 
    ********************************************************************************/
    async createExternalGrades_button(){
      let site_index = document.getElementById('createExternalGrades-site').value;
      let course_index = document.getElementById('createExternalGrades-course').value;
      let url_ending = document.getElementById('createExternalGrades-url_ending').innerHTML;
      /*
      this.openToast();
      this.setToastInfo({
        type: 'success',
        title: 'Create Grade',
        message: 'Successfully Created Grade for ' + String(this.sites_and_courses.courses[course_index].name),
        duration: 6000, 
      });
      */
     
      /*
      await axios.get(`${API_URL}/external_sites_to_course/${course_pk}?id=${profile.auth.profile.id_token}`)
          .then((response)=> {
            let externalSitesToCourse = response.data.result;
            
          })
          .catch((error) => {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'External Grade Error',
              message: 'Can\'t get associated sites to course',
              duration: 6000, 
            });
          });
      */
      
      console.log(this.sites_and_courses.sites[site_index]);
      console.log(this.sites_and_courses.courses[course_index]);
      console.log(url_ending);
    },


    /********************************************************************************   UpdateExternalGrades - ChangeCourse
      updateExternalGrades_changeCourse : Changes the base_url based on dropdown
    ********************************************************************************/
    async updateExternalGrades_changeCourse(){
      let course_index = document.getElementById('updateExternalGrades-course').value;
      this.updateGrade.course_index = course_index;
      let course_pk = this.sites_and_courses.courses[course_index]['pk'];
      const profile = JSON.parse(localStorage.getItem('profile'));
      


      // Get External Site For Selected Course
      axios.get(`${API_URL}/external_sites_to_course/${course_pk}?id=${profile.auth.profile.id_token}`)
        .then((response)=> {
          let externalSitesToCourse = response.data.result;
          let sites = [];
          
          // If single object, function as an array
          if ( !Array.isArray(externalSitesToCourse) )  {
            externalSitesToCourse = [ externalSitesToCourse ];
          }

          externalSitesToCourse.forEach((externalSiteToCourse)=>{
            let site = {
              name: String(externalSiteToCourse.external_site.name) ,
              url: String(externalSiteToCourse.external_site.base_url) + String(externalSiteToCourse.url_ending),
              externalSite_pk: externalSiteToCourse.external_site.id, 
              externalSiteToCourse_pk: externalSiteToCourse.pk
            };
            sites.push(site);
          });
          this.updateGrade.sites = sites;
        })
        .catch((error) => {
          console.log(String(error));
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'External Grade Error',
            message: 'HEY',
            duration: 6000, 
          });
        });



    },
    /********************************************************************************   UpdateExternalGrades - Button
      updateExternalGrades_button: 
    ********************************************************************************/
    updateExternalGrades_button(){
      let course_index = document.getElementById('updateExternalGrades-course').value;
      let site_index = document.getElementById('updateExternalGrades-site').value;

      console.log(this.sites_and_courses.courses[course_index]);
      console.log(this.updateGrade.sites[site_index]);

      this.openToast();
      this.setToastInfo({
        type: 'error',
        title: 'Delete Grade',
        message: 'Failed Delete of ' + this.deleteGrade.sites[site_index].name,
        duration: 6000, 
      });

      
    },


    /********************************************************************************   DeleteExternalGrades - ChangeCourse
      deleteExternalGrades_changeCourse: Changes the base_url based on dropdown
    ********************************************************************************/
    async deleteExternalGrades_changeCourse(){
      let course_index = document.getElementById('deleteExternalGrades-course').value;
      this.deleteGrade.course_index = course_index;
      let course_pk = this.sites_and_courses.courses[course_index]['pk'];
      const profile = JSON.parse(localStorage.getItem('profile'));
      
      // Get External Site For Selected Course
      await axios.get(`${API_URL}/external_sites_to_course/${course_pk}?id=${profile.auth.profile.id_token}`)
        .then((response)=> {
          let externalSitesToCourse = response.data.result;
          let sites = [];
          
          // If single object, function as an array
          if ( !Array.isArray(externalSitesToCourse) )  {
            externalSitesToCourse = [ externalSitesToCourse ];
          }

          externalSitesToCourse.forEach((externalSiteToCourse)=>{
            let site = {
              name: String(externalSiteToCourse.external_site.name) ,
              url: String(externalSiteToCourse.external_site.base_url) + String(externalSiteToCourse.url_ending),
              externalSite_pk: externalSiteToCourse.external_site.id, 
              externalSiteToCourse_pk: externalSiteToCourse.pk
            };
            sites.push(site);
          });
          this.deleteGrade.sites = sites;
        })
        .catch((error) => {
          console.log(String(error));
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'External Grade Error',
            message: 'HEY',
            duration: 6000, 
          });
        });

    },
    /********************************************************************************   DeleteExternalGrades - Button
      deleteExternalGrades_button: 
    ********************************************************************************/
    async deleteExternalGrades_button(){
      const profile = JSON.parse(localStorage.getItem('profile'));
      let course_index = document.getElementById('deleteExternalGrades-course').value;
      let site_index = document.getElementById('deleteExternalGrades-site').value;
      let externalSiteToCourse_pk = this.deleteGrade.sites[site_index].externalSiteToCourse_pk;

      await axios.delete(`${API_URL}/external_import_grades/${externalSiteToCourse_pk}?id_token=${profile.auth.profile.id_token}`)
        .then((response)=> {
          let externalSitesToCourse = response.data.result;

          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Delete Grade',
            message: 'Successfully Deleted ' + this.deleteGrade.sites[site_index].name,
            duration: 6000, 
          });

          this.deleteExternalGrades_changeCourse();
          this.updateExternalGrades_changeCourse();
          
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'External Grade Error',
            message: 'Can\'t get associated sites to course',
            duration: 6000, 
          });
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
  beforeMount(){
    this.getSitesAndCourses();
    //this.getExternalSiteList(); // methods run when  initially loaded
  },
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
