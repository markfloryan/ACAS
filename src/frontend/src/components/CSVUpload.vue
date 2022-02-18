<template>
  <div class="csv-upload">
    <CourseRosterUpload :courseId="courseId" />
    <ActualAssignmentUpload :courseId="courseId" />
    <AssignmentUpload :courseId="courseId" />
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
export default {
  name: 'AddStudentsToCourse',
  components: {
    LoadingLayer,
    CourseRosterUpload,
    AssignmentUpload,
    ActualAssignmentUpload,
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
    };
  },

  methods: {
    // This is used to tell the parent component to change the sub page (change from this addStudents view back to the class graph)
    // *Note: you need to do this because they are not full pages, so you cant just change urls
    changeContext(newContext) {
      this.$emit('contextChange', newContext);
    },
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.csv-upload {
  padding: 8pt;
}
.rostered-students {
  height: 250pt;
  overflow-y: scroll;
}
.not-enrolled-students {
  height: 250pt;
  overflow-y: scroll;
}
</style>
