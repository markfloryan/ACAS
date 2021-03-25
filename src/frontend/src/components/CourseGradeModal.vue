<template>
<!-- TODO: Name is sligly confusing. Maybe change it to CourseGradeInfo? -->
<!-- TODO: Modal currently opens in pull page context, try to use same context as 'TopicModal' -->
  <div v-if="isOpen" class="topic-modal" @click.self="closeModal()">
    <div class="content" style="margin-top: 8pt; overflow-y: scroll">
      <h2 class="title">{{ pageTitle }} Grading Info</h2>
      <sui-icon @click="closeModal()" name="close icon" class="close-modal-button"/>
      <div class="tab-nav">
        <span
          class="link"
          @click="context = 'overview'"
          :style="{ color: context === 'overview' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
        >Overview</span>
    
        <span
          class="link"
          @click="context = 'progress'"
          :style="{ color: context === 'progress' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
        >Progress</span>
        <!-- Only show for professor -->
        <span
          v-if="role === 'professor'"
          class="link"
          @click="context = 'edit_grading_scale'"
          :style="{ color: context === 'edit_grading_scale' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
        >Edit Grading Scale</span>
      </div>
      
      <div class="main">
        <CourseGradeOverview
          v-if="context === 'overview'"
          :role="role"
          :data="data"
          :id="id"
          :letterGrade="letterGrade"
          :numNodesMast="numNodesMast"
          :numNodesComp="numNodesComp"
        />
        <CourseGradeProgress
          v-if="context === 'progress'"
          :role="role"
          :data="data"
          :id="id"
          :letterGrade="letterGrade"
          :numNodesMast="numNodesMast"
          :numNodesComp="numNodesComp"
          :graphData="graphData"
        />
        <CourseGradeEditScale
          v-if="context === 'edit_grading_scale'"
          :role="role"
          :data="data"
          :id="id"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CourseGradeOverview from '@/components/CourseGradeOverview';
import CourseGradeProgress from '@/components/CourseGradeProgress';
import CourseGradeEditScale from '@/components/CourseGradeEditScale';

import { API_URL } from '@/constants';

export default {
  components: {
    CourseGradeOverview,
    CourseGradeProgress,
    CourseGradeEditScale,
  },
  props: {
    role: {
      type: String,
      default: 'professor', // TODO: This seems really dangerous on any page
    },
    data: {
      type: Object,
    },
    isOpen: {
      type: Boolean,
      required: false,
    },
    id: {
      type: String,
      required: true,
    },
    letterGrade: {
      type: String,
      required: true,
    }, 
    numNodesComp: { // TODO: Refactor - These may not all be needed. Maybe can be made smaller
      type: Number,
      required: true,
    },
    numNodesMast: {
      type: Number,
      required: true,
    },
    graphData: {},
  },

  data() {
    return {
      context: 'overview',
      pageTitle: '',
    };
  },

  mounted() {},
  created() {},
  updated() {
    this.pageTitle = this.data.subjectCode + this.data.courseCode;
  },

  methods: {
    closeModal(event) {
      this.$emit('onClose');
    },
  },
};
</script>

<style scoped>
.tab-nav {
  padding-bottom: 8pt;
  margin-bottom: 8pt;
  border-bottom: var(--color-green-10) 0.75pt solid;
}
.tab-nav .link {
  font-weight: bold;
  font-size: 12pt;
  margin-right: 8pt;
  cursor: pointer;
}
.topic-modal {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000000;
  width: 100%;
  height: 100%;
  border-radius: 6pt;
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
  min-width: 500pt;
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
.main {
  height: 100%;
}
</style>
