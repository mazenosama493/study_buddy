 document.addEventListener("DOMContentLoaded", function () {
            // Toggle role-specific fields
            const roleRadios = document.querySelectorAll('input[name="role"]');
            const subjectField = document.getElementById("subject-field");
            const gradeField = document.getElementById("grade-field");

            function toggleFields() {
                subjectField.classList.add("hidden");
                gradeField.classList.add("hidden");

                roleRadios.forEach(radio => {
                    if (radio.checked && radio.value === "teacher") {
                        subjectField.classList.remove("hidden");
                    } else if (radio.checked && radio.value === "student") {
                        gradeField.classList.remove("hidden");
                    }
                });
            }

            roleRadios.forEach(radio => {
                radio.addEventListener("change", toggleFields);
            });

            toggleFields(); // Initialize fields based on default values

            // Custom Dropdown Logic
            const dropdowns = document.querySelectorAll('.custom-dropdown');
            dropdowns.forEach(dropdown => {
                const selected = dropdown.querySelector('.dropdown-selected');
                const options = dropdown.querySelector('.dropdown-options');
                const hiddenInput = dropdown.querySelector('input[type="hidden"]');

                selected.addEventListener('click', () => {
                    options.classList.toggle('active');
                });

                options.querySelectorAll('div').forEach(option => {
                    option.addEventListener('click', () => {
                        selected.textContent = option.textContent;
                        hiddenInput.value = option.dataset.value;

                        // Trigger change event for preview block update
                        if (hiddenInput.id === "id_subject_category") {
                            const subjectPreview = document.getElementById("subject-preview");
                            subjectPreview.textContent = option.textContent || "Mathematics";
                        } else if (hiddenInput.id === "id_grade_level") {
                            const gradePreview = document.getElementById("grade-preview");
                            gradePreview.textContent = `Grade ${option.dataset.value}` || "Grade 1";
                        }

                        options.classList.remove('active');
                    });
                });

                document.addEventListener('click', (event) => {
                    if (!dropdown.contains(event.target)) {
                        options.classList.remove('active');
                    }
                });
            });

            // Update preview block
            const avatarInput = document.getElementById("id_profile_picture");
            const avatarPreview = document.getElementById("avatar-preview");
            const nameInput = document.getElementById("id_username");
            const namePreview = document.getElementById("name-preview");
            const emailInput = document.getElementById("id_email");
            const emailPreview = document.getElementById("email-preview");
            const rolePreview = document.getElementById("role-preview");
            const gradePreview = document.getElementById("grade-preview");
            const subjectPreview = document.getElementById("subject-preview");
            const gradeSubjectPreview = document.getElementById("grade-subject-preview");
            const subjectPreviewText = document.getElementById("subject-preview-text");

            avatarInput.addEventListener("change", function (event) {
                const file = event.target.files[0];
                if (file) {
                    avatarPreview.src = URL.createObjectURL(file);
                }
            });

            nameInput.addEventListener("input", function () {
                namePreview.textContent = nameInput.value || "John Doe";
            });

            emailInput.addEventListener("input", function () {
                emailPreview.textContent = emailInput.value || "example@example.com";
            });

            roleRadios.forEach(radio => {
                radio.addEventListener("change", function () {
                    if (document.querySelector('input[name="role"]:checked')) {
                        const role = document.querySelector('input[name="role"]:checked').value;
                        rolePreview.textContent = role;

                        if (role === "student") {
                            gradeSubjectPreview.classList.remove("hidden");
                            subjectPreviewText.classList.add("hidden");
                        } else if (role === "teacher") {
                            subjectPreviewText.classList.remove("hidden");
                            gradeSubjectPreview.classList.add("hidden");
                        }
                    }
                });
            });
        });