<template>
  <!--
    This is the main page for viewing the details of a class
    THis is where ClassGraph.vue is rendered as well as the option to add students to the course
    or edit the graph for the class
  -->
  <div class="dashboard">
    <!-- Course Selected -->
    <h2 class="title">Class - {{ classData.name ? classData.name : this.id}}</h2>
    
    <!-- Top action buttons-->
    <div class="actions">
      <button
        v-if="isProfessor"
        class="btn btn-plain edit-btn"
        style="margin-left: 8pt;"
        @click="toEdit()"
      >Edit graph</button>
      <button
        v-if="isProfessor && context !== 'courseRoster'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('courseRoster')"
      >Roster</button>
      <button
        v-if="isProfessor && context !== 'csvUpload'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('csvUpload')"
      >CSV</button>
      <button
        v-if="isProfessor && context !== 'classGraph'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('classGraph')"
      >Back to graph</button>
      <h3
        id="grade"
        v-if="this.totalgrade!=0"
      >Grade: {{this.totalgrade}}
      </h3>
    </div>

    <!-- Variable Content -->
    <Sidebar class="sidebar"/>
    <div class="content">
      <CourseRoster
        v-if="context === 'courseRoster'"
        :courseId="id"
        @contextChange="changeContext"
      />
      <CSVUpload
        v-if="context === 'csvUpload'"
        :courseId="id"
        @contextChange="changeContext"
      />
      <!-- TODO: What does id="3" mean? Is it hardcoded? -->
      <ClassGraph
        :hidden="context !== 'classGraph'"
        :id="3" 
        :role="isProfessor ? 'professor' : 'student'"
        :data="graphData"
        @onClose="retrieveClassGraph"
      />
      <h1
        v-if="classNotFound && !isLoading"
        style="text-align: center; margin: auto;"
      >No class graph found :(</h1>
      <LoadingLayer v-if="isLoading" :message="'Fetching course...'"/>
    </div>
  </div>
</template>



<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import CSVUpload from '@/components/CSVUpload';
import CourseRoster from '@/components/CourseRoster';
import ClassGraph from '@/components/ClassGraph';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import { API_URL } from '@/constants';
export default {
  name: 'Course',
  components: {
    CSVUpload,
    CourseRoster,
    ClassGraph,
    LoadingLayer,
    Sidebar,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  data() {
    return {
      classNotFound: true,
      context: 'classGraph',
      classData: {},
      graphData: {},
      isLoading: false,
      isProfessor: false,
      numberofNodes: 0,
      totalgrade: 0,
      file: '',
    };
  },
  created() {
    this.retrieveClassGraph();
  },
  methods: {
    changeContext(newContext) {
      this.context = newContext;
    },
    retrieveClassGraph() {
      // Maybe check if data in vuex, load from there,
      // if not make GET request and then store in vuex?
      this.isProfessor = this.profile.is_professor;
      this.isLoading = true;
      let viewAs = '';
      if (this.$route.query && this.$route.query.viewAs) {
        viewAs = this.$route.query.viewAs;
      }
      axios
        .get(
          `${API_URL}/student/course/?courseId=${
            this.id
          }&view_as=${viewAs}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } }
        )
        .then(data => {
          this.classNotFound = false;
          let classData = data.data.result;
          classData = {
            pk: classData.course.pk,
            name: classData.course.name,
            course_code: classData.course.course_code,
            subject_code: classData.course.subject_code,
            nodes: classData.nodes,
            edges: classData.edges,
          };
          this.totalgrade = data.data.result.grade;
          classData.nodes = classData.nodes.map(node => {
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
        })
        .catch(error => {
          this.classNotFound = true;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    toEdit() {
      this.$router.push({ name: 'Edit', params: { id: this.id } });
    },
    ...mapMutations(
      'toast',
      ['openToast', 'setToastInfo'],
    ),
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    'title title actions'
    'sidebar content content';
  grid-template-columns: 3fr 3fr 7fr;
  grid-template-rows: min-content 1fr;
  height: 100%;
}
.title {
  grid-area: title;
}
.actions {
  grid-area: actions;
}
.actions button {
  float: right;
  white-space: nowrap;
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
  height: calc(100% - 30pt);
  position: relative;
}
#grade {
  float: right;
  display: inline-block;
  transform: translateY(50%);
  margin: auto;
  padding-right: 8pt;
}
</style>
