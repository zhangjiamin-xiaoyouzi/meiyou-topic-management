<template>
  <div class="trial-report-settings">
    <h1>试用报告设置</h1>
    
    <!-- 上交报告预设图片 -->
    <div class="section">
      <div class="label">
        <span class="required">*</span>
        <span>补交报告预设图片：</span>
        <button class="add-btn" @click="showImageUpload = true">添加图片</button>
      </div>
    </div>

    <!-- 第一行设置 -->
    <div class="settings-row">
      <div class="form-group">
        <label class="required">* 报告截止时间</label>
        <div class="input-group">
          <input type="text" placeholder="回复类型" value="回复类型" readonly class="input-readonly">
          <select class="dropdown">
            <option>包括类别</option>
          </select>
          <input type="text" placeholder="请输入内容" class="input-content">
          <span class="unit">天</span>
        </div>
      </div>

      <div class="form-group">
        <label class="required">* 试用报告设置</label>
        <select class="dropdown">
          <option>问卷报告</option>
        </select>
      </div>

      <button class="submit-btn" @click="addQuestionnaire">添加问卷</button>
    </div>

    <!-- 问卷配置区域 -->
    <div class="questionnaires-container">
      <div v-for="(q, index) in questionnaires" :key="index" class="questionnaire-card">
        <div class="form-group">
          <label>标题</label>
          <input v-model="q.title" type="text" class="input-field" placeholder="">
        </div>

        <div class="form-group checkbox-group">
          <label>是否必填</label>
          <input v-model="q.required" type="checkbox" class="checkbox">
        </div>

        <div class="form-group">
          <label>排序值</label>
          <input v-model="q.sortValue" type="text" class="input-field" placeholder="">
        </div>

        <div class="form-group">
          <label>题目类型</label>
          <select v-model="q.questionType" class="dropdown">
            <option value="">请选择</option>
            <option value="text">文本</option>
            <option value="choice">单选</option>
            <option value="multiple">多选</option>
          </select>
        </div>

        <button class="delete-btn" @click="deleteQuestionnaire(index)">删除本问卷</button>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="footer-buttons">
      <button class="save-btn" @click="saveSettings">保存</button>
      <button class="cancel-btn" @click="cancelSettings">取消</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrialReportSettings',
  data() {
    return {
      showImageUpload: false,
      questionnaires: [
        {
          title: '',
          required: false,
          sortValue: '',
          questionType: ''
        },
        {
          title: '',
          required: false,
          sortValue: '',
          questionType: ''
        }
      ]
    }
  },
  methods: {
    addQuestionnaire() {
      this.questionnaires.push({
        title: '',
        required: false,
        sortValue: '',
        questionType: ''
      })
    },
    deleteQuestionnaire(index) {
      this.questionnaires.splice(index, 1)
    },
    saveSettings() {
      console.log('保存设置', this.questionnaires)
      alert('设置已保存')
    },
    cancelSettings() {
      console.log('取消设置')
      alert('已取消')
    }
  }
}
</script>

<style scoped>
.trial-report-settings {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 30px;
  color: #333;
}

.section {
  margin-bottom: 20px;
}

.label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.required {
  color: #ff6b6b;
  font-weight: bold;
}

.add-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.add-btn:hover {
  background-color: #357abd;
}

.settings-row {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  color: #666;
}

.input-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.input-readonly {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f5f5f5;
  color: #999;
  flex: 0 0 auto;
}

.input-content {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.input-field {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.dropdown {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 14px;
}

.unit {
  font-size: 14px;
  color: #666;
  flex: 0 0 auto;
}

.submit-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  align-self: flex-start;
}

.submit-btn:hover {
  background-color: #357abd;
}

.questionnaires-container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 30px;
}

.questionnaire-card {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #eee;
}

.questionnaire-card:last-child {
  margin-bottom: 0;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

.checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.delete-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  margin-top: 15px;
}

.delete-btn:hover {
  background-color: #357abd;
}

.footer-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-start;
}

.save-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background-color: #357abd;
}

.cancel-btn {
  background-color: #999;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #777;
}
</style>
