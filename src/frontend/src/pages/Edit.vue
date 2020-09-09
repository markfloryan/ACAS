<template>
  <div class="dashboard" v-if="isProfessor">
    <h2 class="title">Edit Class: {{classData.name}}</h2>
    <!-- <Sidebar class="sidebar"/> -->
    <div class="content">
      <CreateGraph :id="id" :data="graphData" :classData="classData" :isEditGraph="true" />

      <LoadingLayer v-if="isLoading" :message="'Fetching course...'"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState } from 'vuex';
import CreateGraph from '@/components/CreateGraph';
import LoadingLayer from '@/components/LoadingLayer';
// import Sidebar from '@/components/Sidebar';
import { API_URL } from '@/constants';

export default {
  name: 'Edit',

  components: {
    CreateGraph,
    LoadingLayer,
    // Sidebar,
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  data() {
    return {
      classData: {},
      graphData: {},
      isLoading: false,
    };
  },
  created() {
    // Maybe check if data in vuex, load from there,
    // if not make GET request and then store in vuex?
    this.isProfessor = this.profile.is_professor;
    // console.log(this.profile);
    this.isLoading = true;
    // Get the ID of the student who is logged in
    axios
      .get(`${API_URL}/students/`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
      .then(res => {
        const student_id = res.data.result.pk;
        // Get all topics that are related to the class that they have selected
        axios
          .get(`${API_URL}/student/topics/${this.id}/${student_id}/`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
          .then(studentTopicData => {
            // Get all the data needed about the rest of the class
            axios
              .get(`${API_URL}/courses/${this.id}/`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
              .then(data => {
                this.classNotFound = false;
                if (data && data.data && data.data.result) {
                  let classData = data.data.result;
                  // Recreate the class data with a mixture of the two data sets
                  classData = {
                    pk: classData.pk,
                    name: classData.name,
                    course_code: classData.course_code,
                    subject_code: classData.subject_code,
                    nodes: studentTopicData.data.result,
                    edges: classData.edges,
                  };
                  console.log(classData);
                  classData.nodes = classData.nodes.map(node => {
                    this.numberofNodes += 1;
                    this.totalgrade += node.grade;
                    console.log(node);
                    return {
                      ...node,
                      id: node.pk,
                      grade: node.grade,
                    };
                  });

                  this.graphData = classData;
                  this.classData = {
                    uuid: classData.pk,
                    name: classData.name,
                    courseCode: classData.course_code,
                    subjectCode: classData.subject_code,
                  };
                }
              })
              .catch(error => {
                this.classNotFound = true;
              });
          })
          .catch(error => {
            this.classNotFound = true;
          });
      })
      .catch(error => {
        this.classNotFound = true;
      })
      .finally(() => {
        this.isLoading = false;
      });
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    'title title'
    'content content';
  grid-template-columns: 2fr 10fr;
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
  border-radius: 6pt;

  height: calc(100% - 60pt);
  position: relative;
}
</style>
