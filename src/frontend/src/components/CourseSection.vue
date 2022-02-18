<template>
  <!-- CourseSection.vue
    This component:
      - Is used in the Course.vue page
      - Is an interface for working with course sections
  -->
  <div class="course-roster">
    <br>
    <h3>Sections</h3>
    <div class="rostered-students">
      <sui-table v-if="newSections.length > 0" celled>
        <sui-table-header>
          <sui-table-row>
            <sui-table-header-cell :width="3">Name</sui-table-header-cell>
            <sui-table-header-cell :width="2">Section Code</sui-table-header-cell>
            <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
          </sui-table-row>
        </sui-table-header>
        <sui-table-body>
          <sui-table-row
            v-for="section in newSections" v-bind:key="section.id"
          >
            <sui-table-cell>{{ section.name }}</sui-table-cell>
            <sui-table-cell>{{ section.section_code }}</sui-table-cell>
            <sui-table-cell>
              <center>
                <button @click="editSection(section)" class="btn btn-primary" type="button">Edit</button>
                <button @click="removeSection(section)" class="btn btn-delete" type="button">Remove</button>
              </center>
            </sui-table-cell>
          </sui-table-row>
        </sui-table-body>
      </sui-table>
      <div v-else>
        <p>No sections to show</p>
      </div>
    </div>
    <br>
    <div id="page-navigation">
      <button v-on:click="decrementSectionPage" class="btn" style="padding: 2pt; font-size: 11pt;">Previous</button>
      <input v-model="sectionPageField" placeholder="1" size=1>
      Page: {{ sectionPage }}
      <button v-on:click="incrementSectionPage" class="btn" style="padding: 2pt; font-size: 11pt;" >Next</button>
    </div>
    <br>
    <center>
      <button @click="addSection()" class="btn btn-create">Add Section</button>
    </center>
    <EditSection v-if="popUp" 
      @onClose="closePopUp()" 
      :prefill="currentSection" 
      :create="creating"
      :course="courseId"/>
    <LoadingLayer v-if="isLoading" :message="'Sending...'"/>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import LoadingLayer from '@/components/LoadingLayer';
import EditSection from '@/components/EditSection';
export default {
  name: 'Sections',
  components: {
    LoadingLayer,
    EditSection
  },
  props: {
    courseId: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  data() {
    return {
      isLoading: false,
      popUp: false,
      newSections: [],
      sectionPage: 1,
      sectionPageField: 1,
      currentSection: null,
      creating: false,
    };
  },
  watch: {
    // When the page field. If it is a number greater than zero, change the page number for enrolled students table
    sectionPageField: function (val) {
      var page = parseInt(val);
      if(page != NaN && page >0){
        this.sectionPage = page;
      }
    },
    // When the page number changes, retrieve students with that page number
    sectionPage: function (val) {
      this.retrieveSectionPages(val);
    },
  },
  created() {
    this.retrieveSectionPages(1);
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    // Fills the 'newSections' array with the list of all students enrolled in the class
    // This fills the table on the Edit Class page and allows the professor to remove students
    retrieveSectionPages(page) {
      axios
        .get(`${API_URL}/sections/?courseId=${this.courseId}&page=${page}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          this.newSections = response.data.result;
        })
        .catch(error => {
          console.log(error);
        });
    },
    decrementSectionPage(){
      if(this.sectionPage>1){
        this.sectionPage = this.sectionPage - 1;
      }
    },
    incrementSectionPage(){
      this.sectionPage = this.sectionPage + 1;
    },
    closePopUp(){
      this.retrieveSectionPages(this.sectionPage);
      this.popUp = false;
    },
    editSection(section) {
      this.currentSection = section;
      this.creating = false;
      this.popUp = true;
    },
    addSection() {
      this.currentSection = null;
      this.creating = true;
      this.popUp = true;
    },
    removeSection(section) {
      axios
        .delete(`${API_URL}/sections/${section.pk}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200)
            this.retrieveSectionPages(this.sectionPage);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.course-roster {
  padding: 8pt;
}
.rostered-students {
  height: auto;
  overflow-y: scroll;
}
.not-enrolled-students {
  height: auto;
  overflow-y: scroll;
}
</style>
