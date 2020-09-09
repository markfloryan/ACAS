import Vuex from 'vuex';

import {generate_svg, perc2color} from '@/assets/graph_node_svg.js';

describe('graph_node_svg.js', () => {
  let student_student = {
    first_name: 'student1',
    last_name: 'testStudent',
    username: 'student1',
    is_professor: false,
  };

  let student_professor = {
    first_name: 'professor1',
    last_name: 'testProfessor',
    username: 'professor1',
    is_professor: true,
  };

  let node_unlocked = {
    name: 'unlocked topic',
    grade: 0,
    locked: false,
    student: student_student,
  };

  let node_locked = {
    name: 'locked topic',
    grade: 0,
    locked: true,
    student: student_student,
  };

  let node_unlocked = {
    name: 'unlocked topic',
    grade: 0,
    locked: false,
    student: student_professor,
  };

  let node_locked = {
    name: 'locked topic',
    grade: 0,
    locked: true,
    student: student_professor,
  };
});