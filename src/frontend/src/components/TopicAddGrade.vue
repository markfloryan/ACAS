<template>
  <div class="main">
    <sui-form v-if="role === 'professor'" @submit.prevent>
      <sui-form-field v-if="studentsLoaded">
        <!-- https://semantic-ui-vue.github.io/#/modules/dropdown -->
        <label>Student</label>
        <sui-dropdown
          placeholder="Search students by last name"
          :options="this.studentCollection"
          selection
          search
          v-model="newStudentToAssignment.student"
          @filtered="addGradeStudentFilter"
        />
      </sui-form-field>
      <sui-form-field v-if="assignmentsLoaded">
        <label>Assignment</label>
        <sui-dropdown
          placeholder="Select Assignment"
          :options="this.assignmentCollection"
          selection
          search
          v-model="newStudentToAssignment.assignment"
        />
      </sui-form-field>
      <sui-form-field>
        <label>Grade</label>
        <input placeholder="Enter Grade" v-model="newStudentToAssignment.grade" type="number">
      </sui-form-field>
      <br>
      <button type="button" class="btn btn-create" @click="removeDupStudentToAssignment()">Add/Update Grade</button>
      <br> <br> <br> <br>
      <sui-form-field v-if="studentsLoaded">
        <!-- https://semantic-ui-vue.github.io/#/modules/dropdown -->
        <label>Student</label>
        <sui-dropdown
          placeholder="Search students by last name"
          :options="this.studentCollection"
          selection
          search
          v-model="deleteStudentToAssignment.student"
          @filtered="deleteGradeStudentFilter"
        />
      </sui-form-field>
      <sui-form-field v-if="assignmentsLoaded">
        <label>Assignment</label>
        <sui-dropdown
          placeholder="Select Assignment"
          :options="this.assignmentCollection"
          selection
          search
          v-model="deleteStudentToAssignment.assignment"
        />
      </sui-form-field>
      <br>
      <button type="button" class="btn btn-create" @click="removeStudentToAssignment()">Remove Grade</button>
    </sui-form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
export default {
  components: {},
  props: {
    role: {
      type: String,
      default: 'professor',
    },
    data: {
      type: Object,
    },
    topicId: {
      type: Number,
    },
  },
  data() {
    return {
      studentToTopics: [],
      students: [],
      assignments: [],
      studentCollection: [],
      assignmentCollection: [],
      loaded: false,
      studentsLoaded: false,
      assignmentsLoaded: false,
      newStudentToAssignment: {
        student: null,
        assignment: null,
        grade: null,
      },
      deleteStudentToAssignment: {
        student: null,
        assignment: null,
      },
    };
  },
  mounted() {
    this.getStudents('NULL'); // When mounting, don't filter students by any particular last name
    this.getAssignments();
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
    },
    // Retrieves a list of all students enrolled in the topic
    getStudents(query) {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios
        .get(
          `${API_URL}/student/topics/${this.data.topic.id}?last_name_query=${query}`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        .then(studentResponse => {
          this.studentToTopics = studentResponse.data.result;
          for(let i = 0; i < this.studentToTopics.length; i++) {
            this.students[i] = this.studentToTopics[i].student;
          }
        })
        .catch(error => {
          console.log(error);
        })
        // Parse the students into a form that can be read by the dropdown list
        .finally(() => {
          for(let i = 0; i < this.students.length; i++) {
            this.studentCollection[i] = {value: this.students[i].id, text: this.students[i].first_name + ' ' + this.students[i].last_name};
          }
          this.loaded=true;
          this.studentsLoaded=true;
        });
    },
    // Retrieves a list of all assignments associated with the topic
    getAssignments() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios
        .get(
          `${API_URL}/assignments/?topicId=${this.data.topic.id}`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        .then(assignmentResponse => {
          this.assignments = assignmentResponse.data.result;
        })
        .catch(error => {
          console.log(error);
        })
        // Parse the assignments into a form that can be read by the dropdown list
        .finally(() => {
          for(let i = 0; i < this.assignments.length; i++) {
            this.assignmentCollection[i] = {value: this.assignments[i].pk, text: this.assignments[i].name};
          }
          this.loaded=true;
          this.assignmentsLoaded=true;
        });
    },
    // Adds a student to assignment object to the database when button is pressed (after any duplicate object was deleted)
    addStudentToAssignment() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios
        .post(
          `${API_URL}/studenttoassignments/`, this.newStudentToAssignment, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        // Let the professor know it worked
        .then(response => {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Grade added/updated',
            message: 'The grade was successfully added/updated',
            duration: 6000,
          });
        })
        .catch(error => {
          console.log(error);
          obj.openToast();
          obj.setToastInfo({
            type: 'failure',
            title: 'Error code ' + error.response.status,
            message: 'Something went wrong; check your input and try again',
            duration: 6000,
          });
        });
    },
    // Removes a student to assignment object from the database when button is pressed if that object exists
    removeStudentToAssignment(){
      const profile = JSON.parse(localStorage.getItem('profile'));
      let obj = this;
      axios
        .delete(
          `${API_URL}/studenttoassignments/${this.deleteStudentToAssignment.student}/${this.deleteStudentToAssignment.assignment}`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        .then(response => {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Grade deleted',
            message: 'The grade was successfully deleted',
            duration: 6000,
          });
        })
        .catch(function (error) {
          if(error.response) {
            // Prints a toast clarifying that there was no studentToAssignment to delete
            if(error.response.status == 404) {
              obj.openToast();
              obj.setToastInfo({
                type: 'success',
                title: 'No grade to delete',
                message: 'No grade existed for this student and assignment to delete',
                duration: 6000,
              });
            }
            else {
              console.log(error);
              obj.openToast();
              obj.setToastInfo({
                type: 'failure',
                title: 'Error code ' + error.response.status,
                message: 'Something went wrong; check your input and try again',
                duration: 6000,
              });
            }
          }
        });
    },
    // Checks to make sure there is not a student to assignment object for a given student and assignment before
    // adding a new student to assignment object; if there is, it deletes that object before calling addStudenttoAssignment
    removeDupStudentToAssignment(){
      const profile = JSON.parse(localStorage.getItem('profile'));
      let errorOccured = false;
      axios
        .delete(
          `${API_URL}/studenttoassignments/${this.newStudentToAssignment.student}/${this.newStudentToAssignment.assignment}`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        .catch(function (error) {
          if(error.response) {
            if(error.response.status != 404) {
              console.log(error);
              errorOccured = true;
              obj.openToast();
              obj.setToastInfo({
                type: 'failure',
                title: 'Error code ' + error.response.status,
                message: 'Something went wrong; check your input and try again',
                duration: 6000,
              });
            }
          }
        })
        .finally(() => {
          // As long as no error other than a 404 error occured, the addStudentToAssignment function is called
          if(!errorOccured) {this.addStudentToAssignment();}
        });
    },
    addGradeStudentFilter(val){ // Called when text in the student box for adding grades changes
      if(val!=''){
        this.getStudents(val); // Get students with last names that are like the query string
      }
    },
    deleteGradeStudentFilter(val){ // Called when text in the student box for deleting grades changes
      if(val!=''){
        this.getStudents(val); // Get students with last names that are like the query string
      }
    },
  },
};
</script>

<style scoped>
.main {
  height: 100%;
}
.topic-modal {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000000;
  width: 100%;
  height: 100%;
  background-color: rgba(100, 100, 100, 0.8);
}
.topic-modal > .content {
  grid-area: content;

  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 8pt;
  border-radius: 6pt;

  margin: auto;
  width: 70%;
  min-width: 525pt;
  height: 95%;

  position: relative;
  top: 50%;
  transform: perspective(0.75pt) translateY(-50%);
  padding: 18pt;

  display: grid;
  grid-template-areas:
    'title exit'
    'tabnav tabnav'
    'main main';
  grid-template-rows: min-content min-content 1fr;
  grid-template-columns: 1fr min-content;
}

.topic-modal > .content > .title {
  grid-area: title;
}
.topic-modal > .content > .tab-nav {
  grid-area: tabnav;
}
.topic-modal > .content > .main {
  grid-area: main;
}

.close-modal-button {
  cursor: pointer;
  grid-area: exit;
}
.close-modal-button:hover {
  color: var(--color-blue);
}
</style>
