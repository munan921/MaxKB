<template>
  <el-drawer v-model="visible" size="60%" @close="closeHandle">
    <template #header>
      <h4>{{ $t('views.problem.detailProblem') }}</h4>
    </template>
    <div>
      <el-scrollbar>
        <!-- <Result v-model:loading="loading" :knowledge_id="id" :id="action_id" /> -->
      </el-scrollbar>
    </div>
    <template #footer>
      <div>
        <el-button @click="pre" :disabled="pre_disable || loading">{{
          $t('common.pages.prev')
        }}</el-button>
        <el-button @click="next" :disabled="next_disable || loading">{{
          $t('common.pages.next')
        }}</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Result from '@/views/knowledge-workflow/component/action/Result.vue'
import { MsgSuccess, MsgConfirm, MsgError } from '@/utils/message'
import { loadSharedApi } from '@/utils/dynamics-api/shared-api'
import permissionMap from '@/permission'
import { t } from '@/locales'
const props = withDefaults(
  defineProps<{
    /**
     * 当前的id
     */
    currentId: string
    currentContent: string
    /**
     * 下一条
     */
    next: () => void
    /**
     * 上一条
     */
    pre: () => void

    pre_disable: boolean

    next_disable: boolean
  }>(),
  {},
)

const emit = defineEmits(['update:currentId', 'update:currentContent', 'refresh'])

const route = useRoute()
const {
  params: { id },
} = route

const apiType = computed(() => {
  if (route.path.includes('shared')) {
    return 'systemShare'
  } else if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})

const loading = ref(false)
const visible = ref(false)
const action_id = ref<string>('')

function closeHandle() {
  action_id.value = ''
}

function getRecord() {
  if (props.currentId && visible.value) {
  }
}

watch(
  () => props.currentId,
  () => {
    action_id.value = ''
  },
)

watch(visible, (bool) => {
  if (!bool) {
    emit('update:currentId', '')
    emit('update:currentContent', '')
    emit('refresh')
  }
})

const open = (id: string) => {
  action_id.value = id
  visible.value = true
}

defineExpose({
  open,
})
</script>
<style lang="scss"></style>
