<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTimezone } from '@/composables/useTimezone';
import { getCommonTimezones } from '@/lib/date-utils';
import Card from '@/components/ui/card.vue';
import CardHeader from '@/components/ui/CardHeader.vue';
import CardTitle from '@/components/ui/CardTitle.vue';
import CardDescription from '@/components/ui/CardDescription.vue';
import CardContent from '@/components/ui/CardContent.vue';
import Button from '@/components/ui/button.vue';
import Select from '@/components/ui/select.vue';
import Label from '@/components/ui/label.vue';
import Badge from '@/components/ui/badge.vue';

const { timezone, loading, error, fetchTimezone, updateTimezone } = useTimezone();
const selectedTimezone = ref('');
const saving = ref(false);
const successMessage = ref('');

const timezoneOptions = getCommonTimezones();

onMounted(async () => {
  await fetchTimezone();
  selectedTimezone.value = timezone.value;
});

const handleSave = async () => {
  saving.value = true;
  successMessage.value = '';
  
  const success = await updateTimezone(selectedTimezone.value);
  if (success) {
    successMessage.value = 'Timezone updated successfully!';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  }
  
  saving.value = false;
};
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <div>
      <h2 class="text-3xl font-bold tracking-tight">Timezone Settings</h2>
      <p class="text-muted-foreground mt-2">
        Configure the preferred timezone for displaying and managing shifts.
      </p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Preferred Timezone</CardTitle>
        <CardDescription>
          All shift times will be displayed and managed in this timezone.
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <div class="space-y-2">
          <Label for="timezone">Select Timezone</Label>
          <Select
            id="timezone"
            v-model="selectedTimezone"
            :disabled="loading || saving"
            class="w-full"
          >
            <option v-for="tz in timezoneOptions" :key="tz.value" :value="tz.value">
              {{ tz.label }}
            </option>
          </Select>
        </div>

        <div v-if="timezone" class="flex items-center gap-2 p-4 rounded-lg bg-muted/50">
          <span class="text-sm font-medium">Current Timezone:</span>
          <Badge variant="secondary">{{ timezone }}</Badge>
        </div>

        <div v-if="error" class="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
          <p class="text-sm text-destructive">{{ error }}</p>
        </div>

        <div v-if="successMessage" class="p-4 rounded-lg bg-green-500/10 border border-green-500/20">
          <p class="text-sm text-green-600 dark:text-green-400">{{ successMessage }}</p>
        </div>

        <div class="flex justify-end gap-3">
          <Button
            @click="handleSave"
            :disabled="loading || saving || selectedTimezone === timezone"
            variant="default"
          >
            <span v-if="saving">Saving...</span>
            <span v-else>Save Changes</span>
          </Button>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle>About Timezones</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground">
          When you change the timezone, all existing shifts will be automatically converted
          to the new timezone. This ensures consistency across your shift management system.
        </p>
      </CardContent>
    </Card>
  </div>
</template>

