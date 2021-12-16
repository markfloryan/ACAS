<template>
  <!-- CourseRoster.vue
    This component:
      - Is used in the Course.vue page
      - Is an interface for showing students currently enrolled in the course
      - Allows a professor to add a student to the course being shown in Course.vue
  -->
  <div class="course-roster">
      <br>
      <h3>Enrolled Students</h3>
      <div class="rostered-students">
        <sui-table v-if="newStudents.length > 0" celled>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell :width="2">Name</sui-table-header-cell>
              <sui-table-header-cell :width="2">Email</sui-table-header-cell>
              <sui-table-header-cell :width="3">Sections</sui-table-header-cell>
              <sui-table-header-cell :width="1">Course Grade</sui-table-header-cell>
              <sui-table-header-cell :width="4">Actions</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <sui-table-row
              v-for="student in newStudents" v-bind:key="student.id"
            >
              <sui-table-cell>{{ student.name }}</sui-table-cell>
              <sui-table-cell>{{ student.email }}</sui-table-cell>
              <sui-table-cell>
                <ul class="section">
                  <li v-for="section in student.sections" v-bind:key="section.pk">{{section.name}} - {{section.section_code}}</li>
                </ul>
              </sui-table-cell>
              <sui-table-cell>{{ student.course_grade }}</sui-table-cell>
              <sui-table-cell>
                <button @click="updateSections(student)" class="btn btn-primary" type="button">Sections</button>
                <button @click="removeStudent(student)" class="btn btn-delete" type="button">Remove</button>
              </sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
        <div v-else>
          <p>No students to show</p>
        </div>
      </div>
      <br>
      <div id="page-navigation">
        <button v-on:click="decrementEnrolledPage" class="btn" style="padding: 2pt; font-size: 11pt;">Previous</button>
        <input v-model="enrolledPageField" placeholder="1" size=1>
        Page: {{ enrolledPage }}
        <button v-on:click="incrementEnrolledPage" class="btn" style="padding: 2pt; font-size: 11pt;" >Next</button>
      </div>
      <br>
      <h3>Students not in Class</h3>
      <div class="not-enrolled-students">
        <sui-table v-if="enrollableStudents.length > 0" celled>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell :width="12">Name</sui-table-header-cell>
              <sui-table-header-cell :width="3">Email</sui-table-header-cell>
              <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <sui-table-row
              v-for="student in enrollableStudents" v-bind:key="student.id"
            >
              <sui-table-cell>{{ student.name }}</sui-table-cell>
              <sui-table-cell>{{ student.email }}</sui-table-cell>
              <sui-table-cell>
                <button @click="addStudent(student.value)" class="btn btn-create" type="button">Add</button>
              </sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
        <div v-else>
          <p>No students to show</p>
        </div>
      </div>
      <br>
      <div id="page-navigation">
        <button v-on:click="decrementNotEnrolledPage" class="btn" style="padding: 2pt; font-size: 11pt;">Previous</button>
        <input v-model="notEnrolledPageField" placeholder="1" size=1>
        Page: {{ notEnrolledPage }}
        <button v-on:click="incrementNotEnrolledPage" class="btn" style="padding: 2pt; font-size: 11pt;" >Next</button>
      </div>

    <AddStudentsToSection v-if="addingStudentToSection" 
      @onClose="closePopUp()" 
      :prefill="currentStudent"
      :course="courseId"/>
    <LoadingLayer v-if="isLoading" :message="'Sending...'"/>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';
import CourseRosterUpload from '@/components/CourseRosterUpload';
import AssignmentUpload from '@/components/AssignmentUpload';
import ActualAssignmentUpload from '@/components/ActualAssignmentUpload';
import AddStudentsToSection from '@/components/AddStudentToSections';
export default {
  name: 'AddStudentsToCourse',
  components: {
    LoadingLayer,
    CourseRosterUpload,
    AssignmentUpload,
    ActualAssignmentUpload,
    AddStudentsToSection
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
      addingStudentToSection: false,
      newStudents: [],
      enrollableStudents: [],
      studentRoster: [],
      studentsInClass: {},
      currentStudent: null,
      enrolledPage: 1,
      enrolledPageField: 1,
      notEnrolledPage: 1,
      notEnrolledPageField: 1,
    };
  },
  watch: {
    // When the page field. If it is a number greater than zero, change the page number for enrolled students table
    enrolledPageField: function (val) {
      var page = parseInt(val);
      if(page != NaN && page >0){
        this.enrolledPage = page;
      }
    },
    // When the page number changes, retrieve students with that page number
    enrolledPage: function (val) {
      this.retrieveEnrolledStudents(val);
    },
    notEnrolledPageField: function (val) {
      var page = parseInt(val);
      if(page != NaN && page >0){
        this.notEnrolledPage = page;
      }
    },
    // When the page number changes, retrieve students with that page number
    notEnrolledPage: function (val) {
      this.retrieveNotEnrolledStudents(val);
    },
  },
  created() {
    this.retrieveEnrolledStudents(1).then(this.retrieveNotEnrolledStudents(1));
  },
  methods: {
    // Fills the 'newStudents' array with the list of all students enrolled in the class
    // This fills the table on the Edit Class page and allows the professor to remove students
    retrieveEnrolledStudents(page) {
      return new Promise((resolve, reject) => {
        axios
          .get(`${API_URL}/search/?query=All&courseId=${this.courseId}&page=${page}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } }) // Use this one instead
          .then(response => {
            const data = response.data.result;
            this.newStudents = data.filter(studenttocourse => {
              return (
                studenttocourse && !studenttocourse.student.is_professor
              );
            }).map(studenttocourse => {
              let student = studenttocourse.student;
              student['course_grade'] = studenttocourse.grade;
              return student;
            });
            this.newStudents = this.newStudents.map(student => {
              this.studentsInClass[student.id] = true;
              return {
                value: student.id,
                name: student.first_name + ' ' + student.last_name,
                email: student.email,
                sections: [],
                course_grade: student.course_grade,
              };
            });

            this.newStudents.forEach(student => {
              axios
                .get(`${API_URL}/student/section/?studentId=${student.value}&courseId=${this.courseId}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
                .then(response => {
                  student.sections = response.data.result.map(item => {return item.section;});
                })
                .catch(error => {
                  console.log(error);
                });
            });

            this.quizName = data.name;
            resolve(response);
          })
          .catch(error => {
            this.context = 'courseNotFound';
            reject(error);
          });
      });
    },
    // Fills the 'enrollableStudents' array with the list of all students not enrolled in the class
    // This fills the table on the Edit Class page and allows the professor to add students
    retrieveNotEnrolledStudents(page) {
      return new Promise((resolve, reject) => {
        axios
          .get(`${API_URL}/search/?query=All&courseId=${this.courseId}&invert=1&page=${page}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } }) // Use this one instead
          .then(response => {
            const data = response.data.result;
            this.enrollableStudents = data.filter(student => {
              return (
                student && !student.is_professor
              );
            });
            this.enrollableStudents = this.enrollableStudents.map(student => {
              this.studentsInClass[student.id] = true;
              return {
                value: student.pk,
                name: student.first_name + ' ' + student.last_name,
                email: student.email,
              };
            });
            this.quizName = data.name;
            resolve(response);
          })
          .catch(error => {
            this.context = 'courseNotFound';
            reject(error);
          });
      });
    },
    // This is used to tell the parent component to change the sub page (change from this addStudents view back to the class graph)
    // *Note: you need to do this because they are not full pages, so you cant just change urls
    changeContext(newContext) {
      this.$emit('contextChange', newContext);
    },
    // Does two things:
    // one: it makes the network request to add the given student to the class
    // two: once the student has been saved, it reretireves the student data to rerender the component
    addStudent(student) {
      const data = {
        student: student,
        course: parseInt(this.courseId),
      };
      this.isLoading = true;
      // Add student to the course
      axios
        .post(`${API_URL}/student/course/`, data, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          // Create a relationship between students and all topics in a course
          axios
            .get(`${API_URL}/topics/?courseId=${parseInt(this.courseId)}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
            .then(res => {
              // Res should be all of the topics in a course
              let topicData = Array();
              for (let i = 0; i < res.data.result.length; i++) {
                const element = res.data.result[i];
                let studenttoTopic = {
                  topic: element.pk,
                };
                topicData.push(studenttoTopic);
              }
              const data = {
                // Need to be getting the students id here....
                student: student,
                topics: topicData,
              };
              axios
                .post(`${API_URL}/student/topics/`, data, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
                .then(res => {})
                .catch(error => console.log(error))
                .finally(() => {
                  this.retrieveEnrolledStudents(this.enrolledPage).then(this.retrieveNotEnrolledStudents(this.notEnrolledPage));
                });
            })
            .then(res => {})
            .catch(error => console.log(error));
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          this.selectedStudent = -1;
          this.isLoading = false;
        });
    },
    closePopUp(){
      this.retrieveEnrolledStudents(this.enrolledPage);
      this.addingStudentToSection = false;
    },
    updateSections(student){
      this.currentStudent = student;
      this.addingStudentToSection = true;
    },
    // Does three things:
    // one: it makes the network request to remove the given student from the class
    // two: removes student from sections associated from the class they are being removed from
    // three: once the student has been deleted from the class, it reretireves the student data to rerender the component
    removeStudent(student) {
      axios
        .delete(
          `${API_URL}/student/course/${student.value}?courseId=${parseInt(this.courseId)}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } }
        )
        .then(response => {
          if(response.status == 200) {
            student.sections.forEach(section => {
              axios
                .delete(`${API_URL}/student/section/?sectionId=${section.id}&studentId=${student.value}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
                .then(response => {
                })
                .catch(error => {
                  console.log(error);
                });
            });
          }
        })
        .catch(error => {})
        .finally(() => {
          this.retrieveEnrolledStudents(this.enrolledPage).then(this.retrieveNotEnrolledStudents(this.notEnrolledPage));
        });
    },
    decrementEnrolledPage(){
      if(this.enrolledPage>1){
        this.enrolledPage = this.enrolledPage -1;
      }
    },
    incrementEnrolledPage(){
      this.enrolledPage = this.enrolledPage +1;
    },
    decrementNotEnrolledPage(){
      if(this.notEnrolledPage>1){
        this.notEnrolledPage = this.notEnrolledPage -1;
      }
    },
    incrementNotEnrolledPage(){
      this.notEnrolledPage = this.notEnrolledPage +1;
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
.section {
  display: inline-block;
}
</style>
