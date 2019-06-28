<template>
  <!-- AddStudentsToCourse.vue
    This component:
      - Is used in the Course.vue page
      - Is an interface for showing students currently enrolled in the course
      - Allows a professor to add a student to the course being shown in Course.vue
  -->
  <div class="add-students">
      <CourseRosterUpload :courseId="courseId" />
      <div class="rostered-students">
        <sui-table v-if="newStudents.length > 0" celled>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell :width="2">Index</sui-table-header-cell>
              <sui-table-header-cell :width="12">Name</sui-table-header-cell>
              <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <sui-table-row
              v-for="(student, index) in newStudents"
              :key="`add-student-${student.text}-${index}-tab`"
            >
              <sui-table-cell>{{ index }}</sui-table-cell>
              <sui-table-cell>{{ student.text }}</sui-table-cell>
              <sui-table-cell>
                <button @click="removeStudent(student)" class="btn btn-plain" type="button">Remove</button>
              </sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
      </div>
    
    <LoadingLayer v-if="isLoading" :message="'Sending...'"/>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';
import CourseRosterUpload from '@/components/CourseRosterUpload';

export default {
  name: 'AddStudentsToCourse',

  components: {
    LoadingLayer,
    CourseRosterUpload,
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
      newStudents: [],
      studentRoster: [],
      selectedStudent: -1,
      studentsInClass: {},
    };
  },
  created() {
    this.retrieveEnrolledStudents().then(this.retrieveAllStudents);
  },
  methods: {
    // Fills the 'studentRoster' array with the list of all students on the app
    retrieveAllStudents() {
      return new Promise((resolve, reject) => {
        axios
          .get(`${API_URL}/students/?id_token=${this.profile.id_token}`)
          .then(response => {
            const students = response.data.result;
            this.studentRoster = students.filter((student, index) => {
              console.log({ student });
              return !this.studentsInClass[student.pk] && !student.is_professor;
            });
            this.studentRoster = this.studentRoster.map((student, index) => ({
              text: student.email,
              value: student.pk,
            }));
          })
          .catch(() => {})
          .finally(() => {});
      });
    },
    // Fills the 'newStudents' array with the list of all students on the app, that are not in the class yet
    retrieveEnrolledStudents() {
      return new Promise((resolve, reject) => {
        axios
          .get(`${API_URL}/student/course/?courseId=${this.courseId}`)
          .then(response => {
            const data = response.data.result;
            this.newStudents = data.filter(studentToCourse => {
              return (
                studentToCourse.student && !studentToCourse.student.is_professor
              );
            });
            this.newStudents = this.newStudents.map(studentToCourse => {
              this.studentsInClass[studentToCourse.student.id] = true;
              return {
                value: studentToCourse.student.id,
                text: studentToCourse.student.email,
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
    addStudent() {
      let studentToAdd;
      this.studentRoster.forEach(student => {
        if (student.value === this.selectedStudent) {
          studentToAdd = student;
        }
      });
      const data = {
        student: studentToAdd.value,
        course: parseInt(this.courseId),
      };
      this.isLoading = true;
      // Add student to the course
      axios
        .post(`${API_URL}/student/course/`, data)
        .then(response => {
          // Create a relationship between students and all topics in a course
          axios
            .get(`${API_URL}/topics/?courseId=${parseInt(this.courseId)}`)
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
                student: studentToAdd.value,
                topics: topicData,
              };
              console.log(this.profile);
              axios
                .post(`${API_URL}/student/topics/`, data)
                .then(res => {})
                .catch(error => console.log(error));
            })
            .then(res => {})
            .catch(error => console.log(error));
        })
        .catch(error => {
          consloe.log(error);
        })
        .finally(() => {
          this.studentRoster = this.studentRoster.filter(student => {
            return student.value !== this.selectedStudent;
          });
          this.newStudents.push(studentToAdd);
          this.selectedStudent = -1;
          this.isLoading = false;
        });
    },
    // Does two things:
    // one: it makes the network request to remove the given student from the class
    // two: once the student has been deleted from the class, it reretireves the student data to rerender the component
    removeStudent(student) {
      console.log({ student });
      axios
        .delete(
          `${API_URL}/student/course/${student.value}?courseId=${parseInt(
            this.courseId
          )}&id_token=${this.profile.id_token}`
        )
        .then(response => {})
        .catch(error => {})
        .finally(() => {
          this.retrieveEnrolledStudents().then(this.retrieveAllStudents);
        });
    },
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.add-students {
  padding: 8pt;
}
.rostered-students {
  height: 300pt;
  overflow-y: scroll;
}
</style>
