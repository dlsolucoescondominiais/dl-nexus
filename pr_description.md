🎯 **What:** Added tests for the `register` function in `authService` to ensure error scenarios are correctly handled.
📊 **Coverage:** Added tests to cover the happy path (successful registration), as well as failure scenarios (when Supabase returns an error object, or when an exception is thrown without a message).
✨ **Result:** Improved test coverage and reliability by explicitly verifying that registration errors are formatted into the consistent `{ success: false, data: null, error: ... }` response structure.
