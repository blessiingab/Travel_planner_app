$(document).ready(function() {
  const plansContainer = $('#plansContainer');
  const emptyState = $('#emptyState');
  const toast = new bootstrap.Toast($('#toastMsg')[0]);

  function showToast(message = "Saved successfully!") {
    $('#toastMsg .toast-body').text(message);
    toast.show();
  }

  // Render a single plan card
  function renderPlan(plan) {
    return $(`
      <div class="col" data-id="${plan.id}">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">${plan.destination}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${plan.start_date} to ${plan.end_date}</h6>
            <p class="card-text text-truncate">${plan.activities || 'No activities specified'}</p>
            <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-info btn-sm btn-details" title="View Details"><i class="bi bi-eye"></i></button>
              <button class="btn btn-warning btn-sm btn-edit" title="Edit"><i class="bi bi-pencil"></i></button>
              <button class="btn btn-danger btn-sm btn-delete" title="Delete"><i class="bi bi-trash"></i></button>
            </div>
          </div>
        </div>
      </div>
    `);
  }

  // Load all plans from server and render
  function loadPlans() {
    $.get('/plans', function(data) {
      plansContainer.empty();
      if (data.length === 0) {
        emptyState.show();
      } else {
        emptyState.hide();
        data.forEach(plan => {
          plansContainer.append(renderPlan(plan));
        });
      }
    });
  }

  loadPlans();

  // Add new plan
  $('#planForm').submit(function(e) {
    e.preventDefault();

    const newPlan = {
      destination: $('#destination').val(),
      start_date: $('#start_date').val(),
      end_date: $('#end_date').val(),
      activities: $('#activities').val()
    };

    $.post('/add_plan', newPlan, function(response) {
      if (response.success) {
        loadPlans();
        $('#planForm')[0].reset();
        showToast("Plan added successfully!");
      } else {
        alert("Failed to add plan.");
      }
    });
  });

  // View details modal
  $(document).on('click', '.btn-details', function() {
    const planId = $(this).closest('[data-id]').data('id');
    $.get(`/plan_details/${planId}`, function(data) {
      $('#modalTitle').text(data.destination);
      $('#modalStart').text(data.start_date);
      $('#modalEnd').text(data.end_date);
      $('#modalActivities').text(data.activities || 'None');
      $('#modalWeather').text(data.weather || 'No data');
      const detailsModal = new bootstrap.Modal($('#detailsModal'));
      detailsModal.show();
    });
  });

  // Open edit modal and fill fields
  $(document).on('click', '.btn-edit', function() {
    const planId = $(this).closest('[data-id]').data('id');
    $.get(`/plan_details/${planId}`, function(data) {
      $('#edit_id').val(data.id);
      $('#edit_destination').val(data.destination);
      $('#edit_start_date').val(data.start_date);
      $('#edit_end_date').val(data.end_date);
      $('#edit_activities').val(data.activities);
      const editModal = new bootstrap.Modal($('#editModal'));
      editModal.show();
    });
  });

  // Submit edited plan
  $('#editForm').submit(function(e) {
    e.preventDefault();

    const updatedPlan = {
      id: $('#edit_id').val(),
      destination: $('#edit_destination').val(),
      start_date: $('#edit_start_date').val(),
      end_date: $('#edit_end_date').val(),
      activities: $('#edit_activities').val()
    };

    $.ajax({
      url: `/edit_plan/${updatedPlan.id}`,
      method: 'POST',
      data: updatedPlan,
      success: function(response) {
        if (response.success) {
          loadPlans();
          showToast("Plan updated successfully!");
          const editModalEl = document.getElementById('editModal');
          const editModal = bootstrap.Modal.getInstance(editModalEl);
          editModal.hide();
        } else {
          alert("Failed to update plan.");
        }
      }
    });
  });

  // Delete plan with confirmation
  $(document).on('click', '.btn-delete', function() {
    if (!confirm('Are you sure you want to delete this plan?')) return;

    const planId = $(this).closest('[data-id]').data('id');
    $.ajax({
      url: `/delete_plan/${planId}`,
      method: 'POST',
      success: function(response) {
        if (response.success) {
          loadPlans();
          showToast("Plan deleted.");
        } else {
          alert("Failed to delete plan.");
        }
      }
    });
  });

});
