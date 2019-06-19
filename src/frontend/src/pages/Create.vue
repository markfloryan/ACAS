<template>
  <div class="dashboard">
    <h2 class="title">Create Class</h2>
    <Sidebar class="sidebar"/>
    <div class="content">
      <sui-form @submit.prevent class="create-class-form">
        <sui-form-field>
          <label>Course name</label>
          <input v-model="courseName" placeholder="Course name">
        </sui-form-field>
        <sui-form-field>
          <label>Department code</label>
          <input v-model="courseSubject" placeholder="Department code">
        </sui-form-field>
        <sui-form-field>
          <label>Course code</label>
          <input v-model="courseCode" placeholder="Course Code">
        </sui-form-field>
        <div style="text-align: center;">
          <button
            type="button"
            @click="cancelCourse()"
            style="margin-right: 8pt;"
            class="btn btn-plain cancel-btn"
          >Cancel</button>
          <button type="button" @click="createCourse()" class="btn btn-create create-btn">Create</button>
        </div>
      </sui-form>
    </div>
    <LoadingLayer v-if="loading"
      :message="'Creating course...'" />
  </div>
</template>

<script>
import axios from 'axios';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import { API_URL } from '@/constants';
import { mapGetters, mapState } from 'vuex';

export default {
  name: 'Create',
  components: {
    LoadingLayer,
    Sidebar,
  },
  props: {
    id: {
      type: String,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  data() {
    return {
      courseName: '',
      courseSubject: '',
      courseCode: '',
      loading: false,
      newlyCreatedPk: undefined,
    };
  },
  methods: {
    createCourse() {
      // Insert Post Course to DB
      this.loading = true;
      axios
        .get(`${API_URL}/students/?id_token=${this.profile.id_token}`)
        .then(res => {
          const professor_id = res.data.result.pk;

          let courseData = {
            token: this.profile.id_token,
            pk: 'None',
            name: this.courseName,
            course_code: this.courseCode,
            subject_code: this.courseSubject,
            professor: professor_id,
            nodes: {},
            edges: {},
          };
          axios
            .post(`${API_URL}/courses/`, courseData)
            .then(data => {
              axios
                .get(`${API_URL}/courses/`)
                .then(data => {
                  let courses = data.data.result;
                  let pk;
                  courses.forEach(course => {
                    if (
                      courseData.name === course.name &&
                      courseData.course_code === course.course_code &&
                      courseData.subject_code === course.subject_code
                    ) {
                      pk = course.pk;
                    }
                  });
                  const profile = JSON.parse(localStorage.getItem('profile'));
                  const createRelationshipData = {
                    course: pk,
                    id_token: profile.auth.profile.id_token,
                  };
                  axios
                    .post(`${API_URL}/student/course/`, createRelationshipData)
                    .then(response => {
                      this.$router.push({ name: 'Edit', params: { id: pk } });
                    })
                    .catch(error => {})
                    .finally(() => {
                      this.loading = false;
                    });
                })
                .catch(error => {
                  console.log(error);
                  this.loading = false;
                });
            })
            .catch(error => {
              console.log(error);
              this.loading = false;
            });
        })
        .catch(error => {
          console.log(error);
          this.loading = false;
        })
        .finally(() => {
          console.log('finally');
        });
    },
    addProfessorToNewlyCreatedCourse() {
      return new Promise((resolve, reject) => {
        const data = {
          student: studentToAdd.value,
          course: parseInt(this.courseId),
        };
        this.isLoading = true;
        axios
          .post(`${API_URL}/student/course/`, data)
          .then(response => {
            this.$router.push({ name: 'Edit', params: { id: pk } });
          })
          .catch(error => {})
          .finally(() => {});
      });
    },
    cancelCourse() {
      this.courseName = '';
      this.courseSubject = '';
      this.courseCode = '';
      this.$router.push({ path: '/' });
    },
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    'title title'
    'sidebar content';
  grid-template-columns: 3fr 10fr;
  grid-template-rows: min-content 1fr;
  height: 100%;
}
.title {
  grid-area: title;
}
.sidebar {
  grid-area: sidebar;
  margin-right: 18pt;
}
.content {
  grid-area: content;

  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 8pt;
  border-radius: 6pt;

  height: calc(100% - 30pt);
  position: relative;

  display: grid;
  grid-template-areas: 'form';
}
.create-class-form {
  width: 450pt;
  margin: auto;
  grid-area: form;
}
</style>
