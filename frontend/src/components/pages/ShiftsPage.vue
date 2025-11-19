<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useShifts } from "@/composables/useShifts";
import { useWorkers } from "@/composables/useWorkers";
import { useTimezone } from "@/composables/useTimezone";
import {
    formatDate,
    formatTime,
    localToISO,
    formatDateTimeLocal,
} from "@/lib/date-utils";
import Card from "@/components/ui/card.vue";
import CardHeader from "@/components/ui/CardHeader.vue";
import CardTitle from "@/components/ui/CardTitle.vue";
import CardDescription from "@/components/ui/CardDescription.vue";
import CardContent from "@/components/ui/CardContent.vue";
import Button from "@/components/ui/button.vue";
import Input from "@/components/ui/input.vue";
import Label from "@/components/ui/label.vue";
import Select from "@/components/ui/select.vue";
import Table from "@/components/ui/table.vue";
import TableHeader from "@/components/ui/TableHeader.vue";
import TableBody from "@/components/ui/TableBody.vue";
import TableRow from "@/components/ui/TableRow.vue";
import TableHead from "@/components/ui/TableHead.vue";
import TableCell from "@/components/ui/TableCell.vue";
import Dialog from "@/components/ui/dialog.vue";
import Badge from "@/components/ui/badge.vue";

const {
    shifts,
    loading,
    error,
    fetchShifts,
    createShift,
    updateShift,
    deleteShift,
} = useShifts();
const { workers, fetchWorkers } = useWorkers();
const { timezone } = useTimezone();

const MAX_SHIFT_HOURS = 12;

const getWorkerName = (workerId: string) => {
    return workers.value.find((w) => w.id === workerId)?.name || "Unknown";
};

const computeDurationHours = (startISO: string, endISO: string) => {
    return (new Date(endISO).getTime() - new Date(startISO).getTime()) / 3600000;
};

const formatDuration = (hours: number) => {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    if (m === 0) return `${h}h`;
    return `${h}h ${m}m`;
};

const formatDayKey = (isoString: string) => {
    return new Intl.DateTimeFormat("en-CA", {
        timeZone: timezone.value,
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    }).format(new Date(isoString));
};

const dialogOpen = ref(false);
const editingShift = ref<{
    id: string;
    workerId: string;
    start: string;
    end: string;
} | null>(null);
const selectedWorkerId = ref("");
const startDateTime = ref("");
const endDateTime = ref("");
const filterWorkerId = ref("");
const deletingId = ref<string | null>(null);
const successMessage = ref<string | null>(null);
const formError = ref<string | null>(null);
const confirmDialog = ref<{ open: boolean; shiftId: string | null; worker: string; summary: string }>({
    open: false,
    shiftId: null,
    worker: "",
    summary: "",
});

const todayKey = computed(() => formatDayKey(new Date().toISOString()));

const totalScheduledHours = computed(() =>
    shifts.value.reduce(
        (sum, shift) => sum + (typeof shift.duration === "number" ? shift.duration : computeDurationHours(shift.start, shift.end)),
        0,
    ),
);

const workersScheduledToday = computed(() => {
    const todayShifts = shifts.value.filter((shift) => formatDayKey(shift.start) === todayKey.value);
    return new Set(todayShifts.map((shift) => shift.workerId)).size;
});

const nextShift = computed(() => {
    const now = new Date();
    return (
        [...shifts.value]
            .filter((shift) => new Date(shift.start) > now)
            .sort((a, b) => new Date(a.start).getTime() - new Date(b.start).getTime())[0] ?? null
    );
});

const nextShiftSummary = computed(() => {
    if (!nextShift.value) return "No upcoming shifts";
    return `${getWorkerName(nextShift.value.workerId)} • ${formatDate(nextShift.value.start, timezone.value)} ${formatTime(
        nextShift.value.start,
        timezone.value,
    )}`;
});

const timelineShifts = computed(() => sortedShifts.value.slice(0, 5));

const durationPreview = computed(() => {
    if (!selectedWorkerId.value || !startDateTime.value || !endDateTime.value) {
        return null;
    }

    try {
        const startISO = localToISO(startDateTime.value, timezone.value);
        const endISO = localToISO(endDateTime.value, timezone.value);
        const hours = computeDurationHours(startISO, endISO);
        return {
            startISO,
            endISO,
            hours,
            display: formatDuration(Math.max(hours, 0)),
        };
    } catch (err) {
        return null;
    }
});

const durationWarnings = computed(() => {
    const warnings: string[] = [];
    const preview = durationPreview.value;
    if (!preview) {
        return warnings;
    }

    if (preview.hours <= 0) {
        warnings.push("End time must be after start time.");
    }

    if (preview.hours > MAX_SHIFT_HOURS) {
        warnings.push(`Shifts cannot exceed ${MAX_SHIFT_HOURS} hours.`);
    }

    const overlapsExisting = shifts.value.some((shift) => {
        if (shift.workerId !== selectedWorkerId.value) return false;
        if (editingShift.value && shift.id === editingShift.value.id) return false;
        const shiftStart = new Date(shift.start).getTime();
        const shiftEnd = new Date(shift.end).getTime();
        const newStart = new Date(preview.startISO).getTime();
        const newEnd = new Date(preview.endISO).getTime();
        return newStart < shiftEnd && newEnd > shiftStart;
    });

    if (overlapsExisting) {
        warnings.push("This shift overlaps with another shift for this worker.");
    }

    return warnings;
});

watch([startDateTime, endDateTime, selectedWorkerId], () => {
    if (formError.value) {
        formError.value = null;
    }
});

const showSuccess = (message: string) => {
    successMessage.value = message;
    setTimeout(() => {
        successMessage.value = null;
    }, 3500);
};

const filteredShifts = computed(() => {
    if (!filterWorkerId.value) return shifts.value;
    return shifts.value.filter((s) => s.workerId === filterWorkerId.value);
});

const sortedShifts = computed(() => {
    return [...filteredShifts.value].sort(
        (a, b) => new Date(a.start).getTime() - new Date(b.start).getTime(),
    );
});

onMounted(async () => {
    await Promise.all([fetchWorkers(), fetchShifts()]);
});

const openCreateDialog = () => {
    editingShift.value = null;
    selectedWorkerId.value = filterWorkerId.value || workers.value[0]?.id || "";
    startDateTime.value = "";
    endDateTime.value = "";
    dialogOpen.value = true;
};

const openEditDialog = (shift: {
    id: string;
    workerId: string;
    start: string;
    end: string;
}) => {
    editingShift.value = shift;
    selectedWorkerId.value = shift.workerId;
    startDateTime.value = formatDateTimeLocal(shift.start, timezone.value);
    endDateTime.value = formatDateTimeLocal(shift.end, timezone.value);
    dialogOpen.value = true;
};

const handleSave = async () => {
    if (!selectedWorkerId.value || !startDateTime.value || !endDateTime.value)
        return;

    const startISO = localToISO(startDateTime.value, timezone.value);
    const endISO = localToISO(endDateTime.value, timezone.value);

    if (new Date(endISO) <= new Date(startISO)) {
        formError.value = "End time must be after start time.";
        return;
    }
    formError.value = null;

    if (editingShift.value) {
        await updateShift(editingShift.value.id, {
            workerId: selectedWorkerId.value,
            start: startISO,
            end: endISO,
        });
    } else {
        await createShift({
            workerId: selectedWorkerId.value,
            start: startISO,
            end: endISO,
        });
        showSuccess("Shift added successfully.");
    }

    if (!error.value) {
        dialogOpen.value = false;
        selectedWorkerId.value = "";
        startDateTime.value = "";
        endDateTime.value = "";
        editingShift.value = null;
    }
};

const openDeleteDialog = (shift: { id: string; workerId: string; start: string; end: string }) => {
    confirmDialog.value = {
        open: true,
        shiftId: shift.id,
        worker: getWorkerName(shift.workerId),
        summary: `${formatDate(shift.start, timezone.value)} • ${formatTime(shift.start, timezone.value)} → ${formatTime(shift.end, timezone.value)}`,
    };
};

const closeDeleteDialog = () => {
    confirmDialog.value = { open: false, shiftId: null, worker: "", summary: "" };
};

const confirmDelete = async () => {
    if (!confirmDialog.value.shiftId) return;
    deletingId.value = confirmDialog.value.shiftId;
    await deleteShift(confirmDialog.value.shiftId);
    deletingId.value = null;
    showSuccess("Shift deleted successfully.");
    closeDeleteDialog();
};

</script>

<template>
    <div class="space-y-6">
        <transition name="fade">
            <div
                v-if="successMessage"
                class="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 shadow-sm"
            >
                <div class="flex items-center gap-2">
                    <span class="inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
                    {{ successMessage }}
                </div>
            </div>
        </transition>

        <div class="grid gap-4 md:grid-cols-3">
            <div class="rounded-2xl border border-white shadow-sm bg-white p-4">
                <p class="text-xs uppercase tracking-[0.4em] text-slate-400">Total hours</p>
                <p class="mt-2 text-3xl font-semibold text-slate-900">{{ totalScheduledHours.toFixed(1) }}h</p>
                <p class="text-sm text-slate-500">Across {{ shifts.length }} shifts</p>
            </div>
            <div class="rounded-2xl border border-white shadow-sm bg-white p-4">
                <p class="text-xs uppercase tracking-[0.4em] text-slate-400">Workers today</p>
                <p class="mt-2 text-3xl font-semibold text-slate-900">{{ workersScheduledToday }}</p>
                <p class="text-sm text-slate-500">Scheduled in {{ timezone }} today</p>
            </div>
            <div class="rounded-2xl border border-white shadow-sm bg-white p-4">
                <p class="text-xs uppercase tracking-[0.4em] text-slate-400">Next shift</p>
                <p class="mt-2 text-base font-medium text-slate-900">{{ nextShiftSummary }}</p>
                <p v-if="nextShift" class="text-xs text-slate-500">Duration {{ formatDuration(nextShift.duration ?? computeDurationHours(nextShift.start, nextShift.end)) }}</p>
            </div>
        </div>
        
        <Card v-if="timelineShifts.length">
            <CardHeader>
                <CardTitle>Upcoming timeline</CardTitle>
                <CardDescription>Quick glance of the next few shifts</CardDescription>
            </CardHeader>
            <CardContent>
                <ol class="relative border-l border-slate-200 pl-6">
                    <li
                        v-for="shift in timelineShifts"
                        :key="shift.id"
                        class="mb-6 last:mb-0"
                    >
                        <span class="absolute -left-[9px] mt-1 flex h-4 w-4 items-center justify-center rounded-full border-2 border-sky-400 bg-white"></span>
                        <p class="text-xs uppercase tracking-[0.2em] text-slate-400">
                            {{ formatDate(shift.start, timezone) }}
                        </p>
                        <div class="mt-1 flex flex-wrap items-center gap-2 text-sm text-slate-600">
                            <span class="font-semibold text-slate-900">{{ getWorkerName(shift.workerId) }}</span>
                            <span>
                                {{ formatTime(shift.start, timezone) }} → {{ formatTime(shift.end, timezone) }}
                            </span>
                            <Badge variant="secondary">{{ formatDuration(shift.duration ?? computeDurationHours(shift.start, shift.end)) }}</Badge>
                        </div>
                    </li>
                </ol>
            </CardContent>
        </Card>

        <div
            class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
        >
            <div>
                <h2 class="text-3xl font-bold tracking-tight">Shifts</h2>
                <p class="text-muted-foreground mt-2">
                    Manage working shifts for your team members.
                </p>
            </div>
            <Button
                @click="openCreateDialog"
                size="lg"
                :disabled="workers.length === 0"
            >
                <svg
                    class="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 4v16m8-8H4"
                    />
                </svg>
                Add Shift
            </Button>
        </div>

        <!-- Filter -->
        <Card v-if="workers.length > 0">
            <CardContent class="pt-6">
                <div
                    class="flex flex-col sm:flex-row gap-4 items-start sm:items-center"
                >
                    <div class="flex-1 min-w-0">
                        <Label for="filter-worker">Filter by Worker</Label>
                        <Select
                            id="filter-worker"
                            v-model="filterWorkerId"
                            class="w-full sm:w-auto"
                        >
                            <option value="">All Workers</option>
                            <option
                                v-for="worker in workers"
                                :key="worker.id"
                                :value="worker.id"
                            >
                                {{ worker.name }}
                            </option>
                        </Select>
                    </div>
                    <div class="text-sm text-muted-foreground">
                        Showing {{ filteredShifts.length }} shift{{
                            filteredShifts.length !== 1 ? "s" : ""
                        }}
                    </div>
                </div>
            </CardContent>
        </Card>

        <Card>
            <CardHeader>
                <CardTitle>All Shifts</CardTitle>
                <CardDescription>
                    View and manage all working shifts. Times are displayed in
                    {{ timezone }}.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div
                    v-if="workers.length === 0"
                    class="flex flex-col items-center justify-center py-12 text-center"
                >
                    <div class="rounded-full bg-muted p-6 mb-4">
                        <svg
                            class="h-12 w-12 text-muted-foreground"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                            />
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">No workers yet</h3>
                    <p class="text-muted-foreground mb-4">
                        Create a worker first before adding shifts.
                    </p>
                </div>

                <div
                    v-else-if="loading"
                    class="flex items-center justify-center py-12"
                >
                    <div class="text-muted-foreground">Loading shifts...</div>
                </div>

                <div
                    v-else-if="error"
                    class="p-4 rounded-lg bg-destructive/10 border border-destructive/20"
                >
                    <p class="text-sm text-destructive">{{ error }}</p>
                </div>

                <div
                    v-else-if="sortedShifts.length === 0"
                    class="flex flex-col items-center justify-center py-12 text-center"
                >
                    <div class="rounded-full bg-muted p-6 mb-4">
                        <svg
                            class="h-12 w-12 text-muted-foreground"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">No shifts yet</h3>
                    <p class="text-muted-foreground mb-4">
                        {{
                            filterWorkerId
                                ? "No shifts found for this worker."
                                : "Get started by adding your first shift."
                        }}
                    </p>
                    <Button v-if="!filterWorkerId" @click="openCreateDialog"
                        >Add Shift</Button
                    >
                </div>

                <div v-else class="overflow-x-auto">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Worker</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Start Time</TableHead>
                                <TableHead>End Time</TableHead>
                                <TableHead>Duration</TableHead>
                                <TableHead>Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow
                                v-for="shift in sortedShifts"
                                :key="shift.id"
                            >
                                <TableCell>
                                    <div class="font-medium">
                                        {{ getWorkerName(shift.workerId) }}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="text-sm">
                                        {{ formatDate(shift.start, timezone) }}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="text-sm font-mono">
                                        {{ formatTime(shift.start, timezone) }}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="text-sm font-mono">
                                        {{ formatTime(shift.end, timezone) }}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Badge variant="secondary">{{
                                        formatDuration(shift.duration)
                                    }}</Badge>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center gap-2">
                                        <Button
                                            @click="openEditDialog(shift)"
                                            variant="ghost"
                                            size="sm"
                                        >
                                            <svg
                                                class="h-4 w-4"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                                                />
                                            </svg>
                                            Edit
                                        </Button>
                                        <Button
                                            @click="openDeleteDialog(shift)"
                                            variant="ghost"
                                            size="sm"
                                            :disabled="deletingId === shift.id"
                                        >
                                            <svg
                                                class="h-4 w-4 text-destructive"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                                />
                                            </svg>
                                            Delete
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </div>
            </CardContent>
        </Card>

        <!-- Create/Edit Dialog -->
        <Dialog :open="dialogOpen" @update:open="dialogOpen = $event">
            <div class="space-y-4">
                <div>
                    <h3 class="text-lg font-semibold">
                        {{ editingShift ? "Edit Shift" : "Add New Shift" }}
                    </h3>
                    <p class="text-sm text-muted-foreground mt-1">
                        {{
                            editingShift
                                ? "Update the shift information."
                                : "Create a new shift for a worker."
                        }}
                    </p>
                </div>

                <div class="space-y-2">
                    <Label for="shift-worker">Worker</Label>
                    <Select
                        id="shift-worker"
                        v-model="selectedWorkerId"
                        :disabled="editingShift !== null"
                    >
                        <option value="" disabled>Select a worker</option>
                        <option
                            v-for="worker in workers"
                            :key="worker.id"
                            :value="worker.id"
                        >
                            {{ worker.name }}
                        </option>
                    </Select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="shift-start">Start Date & Time</Label>
                        <Input
                            id="shift-start"
                            v-model="startDateTime"
                            type="datetime-local"
                        />
                    </div>
                    <div class="space-y-2">
                        <Label for="shift-end">End Date & Time</Label>
                        <Input
                            id="shift-end"
                            v-model="endDateTime"
                            type="datetime-local"
                        />
                    </div>
                </div>

                <div class="p-3 rounded-lg bg-muted/50">
                    <p class="text-xs text-muted-foreground">
                        Times are in {{ timezone }} timezone
                    </p>
                </div>

                <div v-if="durationPreview" class="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm">
                    <div>
                        <p class="font-medium text-slate-900">Planned duration</p>
                        <p class="text-slate-500">
                            {{ durationPreview.display }}
                        </p>
                    </div>
                    <Badge :variant="durationWarnings.length ? 'destructive' : 'secondary'">
                        {{ durationWarnings.length ? 'Check details' : 'OK' }}
                    </Badge>
                </div>

                <div v-if="durationWarnings.length" class="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
                    <ul class="list-disc space-y-1 pl-5">
                        <li v-for="warning in durationWarnings" :key="warning">
                            {{ warning }}
                        </li>
                    </ul>
                </div>

                <div
                    v-if="formError || error"
                    class="p-3 rounded-lg border text-sm"
                    :class="formError ? 'border-amber-200 bg-amber-50 text-amber-700' : 'border-destructive/20 bg-destructive/10 text-destructive'"
                >
                    {{ formError || error }}
                </div>

                <div class="flex justify-end gap-3">
                    <Button variant="outline" @click="dialogOpen = false">
                        Cancel
                    </Button>
                    <Button
                        @click="handleSave"
                        :disabled="
                            !selectedWorkerId ||
                            !startDateTime ||
                            !endDateTime ||
                            loading ||
                            durationWarnings.length > 0
                        "
                    >
                        {{ editingShift ? "Update" : "Create" }}
                    </Button>
                </div>
            </div>
        </Dialog>

        <Dialog :open="confirmDialog.open" @update:open="closeDeleteDialog">
            <div class="space-y-4">
                <div>
                    <h3 class="text-lg font-semibold">Delete shift</h3>
                    <p class="text-sm text-muted-foreground">
                        {{ confirmDialog.worker }} • {{ confirmDialog.summary }}
                    </p>
                </div>
                <div class="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
                    This action cannot be undone.
                </div>
                <div class="flex justify-end gap-3">
                    <Button variant="outline" @click="closeDeleteDialog">Cancel</Button>
                    <Button variant="destructive" @click="confirmDelete" :disabled="deletingId === confirmDialog.shiftId">
                        Delete
                    </Button>
                </div>
            </div>
        </Dialog>
    </div>
</template>
