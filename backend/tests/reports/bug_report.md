# Backend Bug Report
**Generated from Unit Test Suite**  
**Last Updated:** December 7, 2025

---

## 📊 Executive Summary

| Metric | Value |
|--------|-------|
| **Total Issues Found** | 8 bugs (BR-001 to BR-010, excluding BR-004) |
| **Test Suite Status** | 63/70 passing (90%) |
| **Docker Environment** | ✅ Fully operational |
| **Test Execution Time** | ~0.54s |

### Issues by Severity

- 🔴 **High Priority (1):** JWT numeric subject validation
- 🟡 **Moderate Priority (4):** Function signature mismatches, empty input handling
- 🟢 **Low Priority (2):** Token timestamp resolution, integration test setup
- 📝 **Legacy (1):** Pydantic v1 incompatibility

---

## 🐛 Active Bugs

### 🔴 BR-009: JWT Numeric Subject Validation Error
**Area:** Authentication | **Priority:** High | **Date:** 2025-12-07

**Problem:**  
The `create_access_token` function rejects numeric subject values, causing token creation to fail when using numeric IDs (like canvas_id).

**How to Reproduce:**
```python
create_access_token({"sub": 12345})  # Fails with InvalidSubjectError
```

**Expected vs Actual:**
- ✅ **Expected:** Accept numeric subjects (RFC 7519 allows this)
- ❌ **Actual:** `jwt.exceptions.InvalidSubjectError: Subject must be a string`

**Impact:**  
High - Any attempt to use numeric IDs as subjects will crash. PyJWT enforces string-only subjects despite JWT spec allowing numbers.

**Workaround:**  
Convert subject to string before passing to `create_access_token`: `{"sub": str(canvas_id)}`

**Related Tests:**
- `test_token_with_numeric_sub` ❌
- `test_token_with_zero_sub` ❌

---

### 🟡 BR-007: Missing User Context Handling
**Area:** AI Tool Helpers | **Priority:** Moderate | **Date:** 2025-12-07

**Problem:**  
`get_overall_grades()` crashes when context doesn't contain a `user` key.

**How to Reproduce:**
```python
await get_overall_grades({})  # Empty context
```

**Expected vs Actual:**
- ✅ **Expected:** Return `[]` or handle gracefully
- ❌ **Actual:** `UnboundLocalError: local variable 'overall_grades' referenced before assignment`

**Impact:**  
Moderate - Any call with empty/missing user context will crash the application.

**Fix Needed:**  
Add defensive null check:
```python
if not context.get("user"):
    return "[]"
```

**Related Tests:**
- `test_get_overall_grades_empty_user` ❌

---

### 🟡 BR-008: Missing Activity Stream Handling
**Area:** AI Tool Helpers | **Priority:** Moderate | **Date:** 2025-12-07

**Problem:**  
`get_activity_stream()` crashes when context lacks `activity_stream` key.

**How to Reproduce:**
```python
await get_activity_stream({}, ["Message"])  # No activity_stream in context
```

**Expected vs Actual:**
- ✅ **Expected:** Return `[]` or handle gracefully
- ❌ **Actual:** `TypeError: 'NoneType' object is not iterable`

**Impact:**  
Moderate - Crashes when activity_stream is missing from context.

**Fix Needed:**  
Add defensive check before iteration.

**Related Tests:**
- `test_get_activity_stream_empty_context` ❌

---

### 🟡 BR-006: Empty Messages List Crash
**Area:** AI Streaming/Moderation | **Priority:** Moderate | **Date:** 2025-12-06

**Problem:**  
`openai_iter_response()` attempts to access `messages[-1]` without checking if the list is empty.

**How to Reproduce:**
```python
await openai_iter_response([], "", context)
```

**Expected vs Actual:**
- ✅ **Expected:** Yield nothing or handle gracefully
- ❌ **Actual:** `IndexError: list index out of range`

**Impact:**  
Moderate - Empty messages list crashes the streaming function.

**Fix Needed:**  
Check `if messages:` before accessing `messages[-1]`.

**Related Tests:**
- `test_openai_iter_response_empty_messages` ⚠️ (marked xfail)

---

### 🟡 BR-001, BR-002, BR-003: Function Signature Mismatches
**Area:** AI Tool Helpers | **Priority:** Moderate | **Date:** 2025-12-06

**Problem:**  
Tests call AI helper functions with incorrect parameters, revealing confusion about function signatures.

| Bug | Function | Wrong Call | Correct Signature |
|-----|----------|------------|-------------------|
| BR-001 | `get_assignments` | `get_assignments([courses])` | `get_assignments(context)` |
| BR-002 | `get_activity_stream` | `get_activity_stream(events)` | `get_activity_stream(context, activities)` |
| BR-003 | `get_overall_grades` | `get_overall_grades([courses])` | `get_overall_grades(context)` |

**Impact:**  
Moderate - Tests need updating to match actual API. May indicate documentation gaps.

**Action:**  
Update test suite to use correct context-based signatures.

---

### 🟢 BR-010: Legacy Integration Test Failures
**Area:** Test Infrastructure | **Priority:** Low | **Date:** 2025-12-07

**Problem:**  
Legacy integration tests fail with authentication/database errors.

**Failing Tests:**
- `test_save_chat_session` → Returns 401 Unauthorized (expected 200)
- `test_get_current_user` → Returns 404 Not Found (expected 200)

**Impact:**  
Low - Test infrastructure issue, not production code bug. Tests may need real MongoDB connection or updated fixtures.

**Action:**  
Update test fixtures or mark as integration tests requiring database.

---

### 🟢 BR-005: Token Timestamp Resolution
**Area:** Authentication | **Priority:** Low | **Date:** 2025-12-06

**Problem:**  
Tokens created in rapid succession (within same second) have identical `iat` timestamps.

**Impact:**  
Low - Unix timestamp has 1-second resolution. Minimal impact on normal usage.

**Note:**  
This is a design limitation, not necessarily a bug. Consider millisecond precision if token uniqueness is critical.

---

## 🎯 Recommended Fixes (Priority Order)

1. **🔴 High Priority**
   - [ ] Convert numeric subjects to strings in `create_access_token` (BR-009)

2. **🟡 Moderate Priority**
   - [ ] Add null checks in `get_overall_grades` (BR-007)
   - [ ] Add null checks in `get_activity_stream` (BR-008)
   - [ ] Add empty list check in `openai_iter_response` (BR-006)
   - [ ] Update test signatures for AI helpers (BR-001, BR-002, BR-003)

3. **🟢 Low Priority**
   - [ ] Fix or update legacy integration tests (BR-010)
   - [ ] Consider millisecond timestamps for tokens (BR-005)

---

## 📈 Test Suite Status

### Overall Metrics
- **Total Tests:** 70 (64 unit + 6 legacy integration)
- **Passing:** 63 (90%)
- **Failing:** 6 (9%)
- **Expected Failures:** 1 (1%)
- **Docker Environment:** ✅ Operational

### Coverage by Module

| Test File | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| `test_ai_unit.py` | 8 | 100% | ✅ All passing |
| `test_auth_unit.py` | 2 | 100% | ✅ All passing |
| `test_jwt_unit.py` | 14 | 100% | ✅ All passing |
| `test_utils_unit.py` | 20 | 100% | ⚠️ 2 failing (BR-009) |
| `test_endpoints_unit.py` | 2 | 100% | ✅ All passing |
| `test_negative_cases_unit.py` | 12 | 96% | ⚠️ 2 failing (BR-007, BR-008) |
| Legacy tests | 6 | — | ⚠️ 2 failing (BR-010) |

### Currently Failing Tests

| Test | Bug ID | Reason |
|------|--------|--------|
| `test_openai_iter_response_empty_messages` | BR-006 | ⚠️ Expected failure (xfail) |
| `test_get_overall_grades_empty_user` | BR-007 | UnboundLocalError on empty context |
| `test_get_activity_stream_empty_context` | BR-008 | TypeError on missing activity_stream |
| `test_token_with_numeric_sub` | BR-009 | JWT rejects numeric subject |
| `test_token_with_zero_sub` | BR-009 | JWT rejects zero as subject |
| `test_save_chat_session` | BR-010 | Integration test auth issue |
| `test_get_current_user` | BR-010 | Integration test 404 error |

---

## 🔧 Test Infrastructure

### Docker Environment Status: ✅ Operational

All stub issues have been resolved:
- ✅ MongoDB client is subscriptable (`_StubAsyncIOMotorClient.__getitem__`)
- ✅ Added `drop_database()` method to MongoDB stub
- ✅ CORS middleware matches ASGI3 signature
- ✅ Real `fastapi.testclient.TestClient` available for legacy tests
- ✅ Fixed `app.mongodb` attribute initialization
- ✅ Using real models (removed models stub for FastAPI/Pydantic validation)

### Test Execution

```bash
# Run all tests in Docker
cd backend && docker build -f testing.Dockerfile -t ai-tutor-tests . && \
docker run --rm ai-tutor-tests pytest tests -v

# Run only unit tests
docker run --rm ai-tutor-tests pytest tests/UnitTests -v

# Run with coverage
docker run --rm ai-tutor-tests pytest tests --cov=. --cov-report=term
```

---

## 📝 Notes

- Overall backend coverage: ~42% (diluted by legacy modules)
- Unit test files themselves: 96-100% coverage
- All tests run successfully in Docker containerized environment
- Both isolated unit tests and integration tests can run together
- Stub infrastructure is production-ready and maintainable

