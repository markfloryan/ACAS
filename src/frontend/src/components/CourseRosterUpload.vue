<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  /*
  Defines the data used by the component
  */
  data(){
    return {
      file: ''
    }
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
  },

  methods: {
    /*
    Submits the file to the server
    */
    submitFile(){
      /*
      Initialize the form data
      */
      let formData = new FormData();

      /*
      Add the form data we need to submit
      */
      formData.append('file', this.file);
      formData.append('token', this.profile.id_token);

      /*
      Make the request to the POST /single-file URL
      */
      axios
      .post( `${ API_URL }/courseRosterUpload/${ this.courseId }/`,
        formData,
          {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
        }
      ).then(result => {
        console.log('SUCCESS!!');
        console.log(result);
      })
      .catch(err => {
        console.log('FAILURE!!');
        console.log(err.response);
      });
    },

    /*
      Handles a change on the file upload
    */
    handleFileUpload(){
      this.file = this.$refs.file.files[0];
    }
  } 
}
  </script>